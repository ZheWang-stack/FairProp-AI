import json
import re
import os
import logging
import hashlib
from typing import List, Dict, Any, Union, TypedDict
from functools import lru_cache

# Fallback for fuzzy matching
try:
    from thefuzz import fuzz
    HAS_THEFUZZ = True
except ImportError:
    import difflib
    HAS_THEFUZZ = False

# OCR
try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

from .models import ModelManager

# Configure logging with more granular levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("fairprop.auditor")

class FlaggedItem(TypedDict):
    id: str
    category: str
    trigger_words: List[str]
    found_word: str
    severity: str
    legal_basis: str
    suggestion: str

class AuditReport(TypedDict):
    score: int
    flagged_items: List[FlaggedItem]
    is_safe: bool

class FairHousingAuditor:
    """
    A professional auditor class to scan real estate listings for Fair Housing Act (FHA) violations.
    
    This auditor uses a Neuro-Symbolic AI architecture combining:
    1. Rule-based keyword matching (fast, deterministic)
    2. Semantic vector search (catches paraphrases and implicit bias)
    3. Zero-shot classification (detects discriminatory intent)
    
    The multi-layered approach ensures both high precision and recall,
    catching both obvious violations and subtle steering language.
    """

    def __init__(self, rules_path: str = "fha_rules.json", similarity_threshold: float = 0.85, jurisdictions: list = None, language: str = 'en'):
        """
        Initializes the auditor with specified configuration.
        
        Args:
            rules_path: Path to federal FHA rules JSON file
            similarity_threshold: Cosine similarity threshold for semantic matching (0.0-1.0)
            jurisdictions: List of additional jurisdictions to load (e.g., ['california', 'nyc', 'uk'])
            language: Language code for i18n support (default: 'en')
        
        Note:
            The auditor uses lazy loading for AI models to keep startup fast.
            Models are only loaded when actually needed for scanning.
        """
        self.rules_path = rules_path
        self.similarity_threshold = similarity_threshold
        self.fuzz_threshold = 0.85  # Fuzzy matching threshold for typos/variations
        self.jurisdictions = jurisdictions or []
        self.language = language
        
        # Initialize i18n for multi-language support
        try:
            from .i18n import get_i18n
            self.i18n = get_i18n(language)
            logger.debug("i18n initialized for language: %s", language)
        except ImportError:
            logger.warning("i18n module not available, falling back to English")
            self.i18n = None
        
        # Load federal rules first, then merge jurisdiction-specific rules
        # This allows us to support multi-jurisdiction compliance in a single scan
        self.rules = self._load_rules()
        logger.info("Loaded %s total rules (federal + %s jurisdictions)", len(self.rules), len(self.jurisdictions))
        
        # Get singleton ModelManager instance (handles lazy loading of heavy AI models)
        self.model_manager = ModelManager.get_instance()
        
        # Initialize semantic layer if AI dependencies are available
        # This creates the vector database for semantic search
        if self.model_manager.has_ai:
            logger.debug("AI engines available, initializing vector database...")
            _ = self.model_manager.get_collection(self.rules)
        else:
            logger.info("Running in rule-only mode (AI dependencies not found)")
    
    def reload_rules(self):
        """
        Hot-reload rules from disk without restarting the service.
        
        This is useful for updating rules in production without downtime.
        The vector database is automatically re-indexed with new rules.
        """
        logger.info("Hot-reloading rules from disk...")
        old_count = len(self.rules)
        self.rules = self._load_rules()
        new_count = len(self.rules)
        
        # Re-index into vector database if AI is available
        if self.model_manager.has_ai:
            logger.info("Re-indexing rules into vector database...")
            # Force recreation of collection
            self.model_manager.reset_collection()
            _ = self.model_manager.get_collection(self.rules)
        
        logger.info("Rules reloaded: %s -> %s rules", old_count, new_count)
        return {"old_count": old_count, "new_count": new_count}

    def _load_rules(self) -> List[Dict[str, Any]]:
        """Loads FHA rules from the JSON configuration and merges jurisdiction-specific rules."""
        if not os.path.exists(self.rules_path):
            # Try looking in current working directory if not found
            cwd_path = os.path.join(os.getcwd(), self.rules_path)
            if os.path.exists(cwd_path):
                self.rules_path = cwd_path
            else:
                logger.error("Rules database not found at %s", self.rules_path)
                raise FileNotFoundError(f"Rules database not found at {self.rules_path}")
        
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                federal_rules = json.load(f)
        except json.JSONDecodeError as e:
            logger.error("Error parsing rules file: %s", e)
            raise ValueError(f"Error parsing rules file: {e}") from e
        
        # Load jurisdiction-specific rules
        all_rules = federal_rules.copy()
        
        # Comprehensive jurisdiction mapping
        jurisdiction_map = {
            # US State/City - Major jurisdictions
            'california': 'rules/california_feha.json',
            'nyc': 'rules/nyc_hrl.json',
            'new_york_city': 'rules/nyc_hrl.json',
            
            # All 50 US States + DC (auto-generated)
            'alabama': 'rules/us_states/alabama.json',
            'alaska': 'rules/us_states/alaska.json',
            'arizona': 'rules/us_states/arizona.json',
            'arkansas': 'rules/us_states/arkansas.json',
            'colorado': 'rules/us_states/colorado.json',
            'connecticut': 'rules/us_states/connecticut.json',
            'delaware': 'rules/us_states/delaware.json',
            'dc': 'rules/us_states/dc.json',
            'washington_dc': 'rules/us_states/dc.json',
            'florida': 'rules/us_states/florida.json',
            'georgia': 'rules/us_states/georgia.json',
            'hawaii': 'rules/us_states/hawaii.json',
            'idaho': 'rules/us_states/idaho.json',
            'illinois': 'rules/us_states/illinois.json',
            'indiana': 'rules/us_states/indiana.json',
            'iowa': 'rules/us_states/iowa.json',
            'kansas': 'rules/us_states/kansas.json',
            'kentucky': 'rules/us_states/kentucky.json',
            'louisiana': 'rules/us_states/louisiana.json',
            'maine': 'rules/us_states/maine.json',
            'maryland': 'rules/us_states/maryland.json',
            'massachusetts': 'rules/us_states/massachusetts.json',
            'michigan': 'rules/us_states/michigan.json',
            'minnesota': 'rules/us_states/minnesota.json',
            'mississippi': 'rules/us_states/mississippi.json',
            'missouri': 'rules/us_states/missouri.json',
            'montana': 'rules/us_states/montana.json',
            'nebraska': 'rules/us_states/nebraska.json',
            'nevada': 'rules/us_states/nevada.json',
            'new_hampshire': 'rules/us_states/new_hampshire.json',
            'new_jersey': 'rules/us_states/new_jersey.json',
            'new_mexico': 'rules/us_states/new_mexico.json',
            'new_york': 'rules/us_states/new_york.json',
            'north_carolina': 'rules/us_states/north_carolina.json',
            'north_dakota': 'rules/us_states/north_dakota.json',
            'ohio': 'rules/us_states/ohio.json',
            'oklahoma': 'rules/us_states/oklahoma.json',
            'oregon': 'rules/us_states/oregon.json',
            'pennsylvania': 'rules/us_states/pennsylvania.json',
            'rhode_island': 'rules/us_states/rhode_island.json',
            'south_carolina': 'rules/us_states/south_carolina.json',
            'south_dakota': 'rules/us_states/south_dakota.json',
            'tennessee': 'rules/us_states/tennessee.json',
            'texas': 'rules/us_states/texas.json',
            'utah': 'rules/us_states/utah.json',
            'vermont': 'rules/us_states/vermont.json',
            'virginia': 'rules/us_states/virginia.json',
            'washington': 'rules/us_states/washington.json',
            'west_virginia': 'rules/us_states/west_virginia.json',
            'wisconsin': 'rules/us_states/wisconsin.json',
            'wyoming': 'rules/us_states/wyoming.json',
            
            # International - Countries
            'canada': 'rules/international/canada.json',
            'australia': 'rules/international/australia.json',
            'uk': 'rules/international/uk.json',
            'united_kingdom': 'rules/international/uk.json',
            'singapore': 'rules/international/asia_pacific.json',
            'hong_kong': 'rules/international/asia_pacific.json',
            'japan': 'rules/international/asia_pacific.json',
            'asia_pacific': 'rules/international/asia_pacific.json',
            
            # European Union
            'germany': 'rules/international/germany.json',
            'deutschland': 'rules/international/germany.json',
            'france': 'rules/international/france.json',
            'netherlands': 'rules/international/netherlands.json',
            'nederland': 'rules/international/netherlands.json',
            
            # Europe (Additional)
            'spain': 'rules/international/spain.json',
            'italy': 'rules/international/italy.json',
            'portugal': 'rules/international/portugal.json',
            'poland': 'rules/international/poland.json',
            'sweden': 'rules/international/sweden.json',
            'norway': 'rules/international/norway.json',
            'denmark': 'rules/international/denmark.json',
            'finland': 'rules/international/finland.json',
            'belgium': 'rules/international/belgium.json',
            'austria': 'rules/international/austria.json',
            'switzerland': 'rules/international/switzerland.json',
            'ireland': 'rules/international/ireland.json',
            'greece': 'rules/international/greece.json',
            'czech_republic': 'rules/international/czech_republic.json',
            
            # Asia
            'china': 'rules/international/china.json',
            'india': 'rules/international/india.json',
            'south_korea': 'rules/international/south_korea.json',
            'korea': 'rules/international/south_korea.json',
            'thailand': 'rules/international/thailand.json',
            'vietnam': 'rules/international/vietnam.json',
            'indonesia': 'rules/international/indonesia.json',
            'malaysia': 'rules/international/malaysia.json',
            'philippines': 'rules/international/philippines.json',
            'taiwan': 'rules/international/taiwan.json',
            
            # Middle East
            'uae': 'rules/international/uae.json',
            'saudi_arabia': 'rules/international/saudi_arabia.json',
            'israel': 'rules/international/israel.json',
            'turkey': 'rules/international/turkey.json',
            
            # Africa
            'south_africa': 'rules/international/south_africa.json',
            'nigeria': 'rules/international/nigeria.json',
            'kenya': 'rules/international/kenya.json',
            'egypt': 'rules/international/egypt.json',
            'morocco': 'rules/international/morocco.json',
            
            # Latin America
            'brazil': 'rules/international/brazil.json',
            'brasil': 'rules/international/brazil.json',
            'mexico': 'rules/international/mexico.json',
            'méxico': 'rules/international/mexico.json',
            'argentina': 'rules/international/argentina.json',
            'chile': 'rules/international/chile.json',
            'colombia': 'rules/international/colombia.json',
            'peru': 'rules/international/peru.json',
            'costa_rica': 'rules/international/costa_rica.json',
            'panama': 'rules/international/panama.json',
            
            # Oceania
            'new_zealand': 'rules/international/new_zealand.json',
        }
        
        for jurisdiction in self.jurisdictions:
            jurisdiction_lower = jurisdiction.lower()
            if jurisdiction_lower in jurisdiction_map:
                jurisdiction_path = jurisdiction_map[jurisdiction_lower]
                full_path = os.path.join(os.path.dirname(self.rules_path), '..', jurisdiction_path)
                
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            jurisdiction_rules = json.load(f)
                            all_rules.extend(jurisdiction_rules)
                            logger.info(f"Loaded {len(jurisdiction_rules)} rules for {jurisdiction}")
                    except Exception as e:
                        logger.warning(f"Failed to load {jurisdiction} rules: {e}")
                else:
                    logger.warning(f"Jurisdiction rules not found: {full_path}")
        
        return all_rules

    def suggest_fix(self, text: str) -> str:
        """Uses generative AI to rewrite a problematic listing."""
        if not self.model_manager.has_ai or not self.model_manager.fixer_pipeline:
            return "AI Fixer not available. Please manually revise based on suggestions."

        try:
            fixer = self.model_manager.fixer_pipeline
            prompt = (
                f"Rewrite the following real estate listing description to be strictly compliant with the US Fair Housing Act (FHA). "
                f"Remove any language that implies preference, limitation, or discrimination based on race, color, religion, sex, handicap, familial status, or national origin. "
                f"Maintain the appealing tone of the property description but use neutral, inclusive terminology. "
                f"\n\nListing Text: {text}"
            )
            result = fixer(prompt, max_length=200, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            logger.error(f"AI Fix failed: {e}")
            return f"(AI Fix failed: {str(e)})"

    
    def _generate_cache_key(self, text: str) -> str:
        """
        Generate a cache key for the given text.
        Uses SHA-256 hash to create a unique, deterministic key.
        """
        # Include jurisdictions in cache key to avoid cross-jurisdiction cache hits
        cache_input = f"{text}:{','.join(sorted(self.jurisdictions))}"
        return hashlib.sha256(cache_input.encode('utf-8')).hexdigest()
    
    @lru_cache(maxsize=1000)
    def _scan_text_cached(self, text_hash: str, text: str) -> AuditReport:
        """
        Internal cached version of scan_text.
        
        The text_hash parameter ensures cache invalidation when text changes,
        while the actual text is used for scanning.
        """
        return self._scan_text_impl(text)
    
    def scan_text(self, text: str, use_cache: bool = True) -> AuditReport:
        """
        Scans input text for FHA violations.
        
        This method implements a three-layer detection system:
        1. Keyword/Fuzzy Matching: Fast detection of explicit violations
        2. Semantic Vector Search: Catches paraphrases and implicit bias
        3. Neural Guardrail: Zero-shot classification for discriminatory intent
        
        Args:
            text: The listing text to scan
            use_cache: Whether to use caching (default: True)
        
        Returns:
            AuditReport with score, flagged items, and safety status
        
        Note:
            Caching is enabled by default to improve performance for repeated scans.
            The cache uses LRU eviction and stores up to 1000 recent scans.
        """
        if use_cache:
            text_hash = self._generate_cache_key(text)
            return self._scan_text_cached(text_hash, text)
        else:
            return self._scan_text_impl(text)
    
    def _scan_text_impl(self, text: str) -> AuditReport:
        """
        Internal implementation of text scanning (uncached).
        
        This is separated from scan_text() to allow caching to work properly
        with the @lru_cache decorator.
        """
        flagged_items = []
        flagged_rule_ids = set()
        score = 100
        
        # 1. Keyword/Fuzzy Matching
        words = re.findall(r'\w+', text.lower())
        for rule in self.rules:
            if rule["id"] in flagged_rule_ids: continue
                
            for trigger in rule["trigger_words"]:
                for word in words:
                    if self._fuzzy_match(trigger.lower(), word):
                        item = self._create_flag(rule, trigger, word)
                        flagged_items.append(item)
                        flagged_rule_ids.add(rule["id"])
                        break
                if rule["id"] in flagged_rule_ids: break

        # 2. Semantic Vector Search
        if self.model_manager.has_ai:
            collection = self.model_manager.get_collection(self.rules)
            if collection:
                sentences = [s.strip() for s in re.split(r'[.!?\n]', text) if len(s.strip()) > 10]
                if sentences:
                    try:
                        results = collection.query(
                            query_texts=sentences,
                            n_results=1,
                            include=["metadatas", "distances", "documents"]
                        )
                        for i, sentence in enumerate(sentences):
                            if not results['distances'][i]: continue
                            
                            distance = results['distances'][i][0]
                            metadata = results['metadatas'][i][0]
                            matched_trigger = results['documents'][i][0]
                            
                            # Heuristic for cosine similarity from Chroma's default L2
                            similarity = 1 - (distance / 2)
                            
                            if similarity >= self.similarity_threshold:
                                rule_id = metadata["rule_id"]
                                if rule_id not in flagged_rule_ids:
                                    rule = next((r for r in self.rules if r["id"] == rule_id), None)
                                    if rule:
                                        item = self._create_flag(rule, matched_trigger, sentence)
                                        item["suggestion"] += " (Detected via semantic analysis)"
                                        flagged_items.append(item)
                                        flagged_rule_ids.add(rule_id)
                    except Exception as e:
                        logger.warning(f"Semantic search failed: {e}")

        # 3. Neural Guardrail (Intent/Steering Detection via Zero-Shot)
        if self.model_manager.has_ai and self.model_manager.guardrail_pipeline:
            guardrail = self.model_manager.guardrail_pipeline
            sentences = [s.strip() for s in re.split(r'[.!?\n]', text) if len(s.strip()) > 15]
            
            # Labels we want to detect presence of
            candidate_labels = ["discriminatory", "exclusionary", "restrictive", "welcoming", "inclusive"]

            for sentence in sentences:
                try:
                    # distinct from sentiment - we ask "Is this sentence discriminatory or exclusionary?"
                    result = guardrail(sentence, candidate_labels)
                    
                    # Result structure: {'labels': [...], 'scores': [...]}
                    # We check if the top label is negative (discriminatory/exclusionary/restrictive) with high confidence
                    top_label = result['labels'][0]
                    top_score = result['scores'][0]
                    
                    if top_label in ["discriminatory", "exclusionary", "restrictive"] and top_score > 0.85:
                        neural_flag: FlaggedItem = {
                            "id": "NEURAL-ZERO-SHOT",
                            "category": f"Potential {top_label} language",
                            "trigger_words": ["(AI Intent Analysis)"],
                            "found_word": sentence[:50] + "...",
                            "severity": "Critical",
                            "legal_basis": f"AI model detected high probability ({top_score:.2f}) of {top_label} intent.",
                            "suggestion": "Review tone to ensuring it is welcoming and inclusive to all protected classes."
                        }
                        flagged_items.append(neural_flag)
                        # Break after finding significant automated flag to avoid noise
                        break
                except Exception as e:
                    logger.warning(f"Neural guardrail failed: {e}")

        # 4. Scoring
        for item in flagged_items:
            penalty = 25 if item["severity"] == "Critical" else 10
            score = max(0, score - penalty)

        return {
            "score": score,
            "flagged_items": flagged_items,
            "is_safe": score >= 70
        }

    def _fuzzy_match(self, rule_word: str, text_word: str) -> bool:
        if ' ' in rule_word or len(rule_word) < 4: return False
        if HAS_THEFUZZ:
            return fuzz.ratio(rule_word, text_word) >= (self.fuzz_threshold * 100)
        else:
            return difflib.SequenceMatcher(None, rule_word, text_word).ratio() >= self.fuzz_threshold

    def _create_flag(self, rule: Dict[str, Any], trigger: str, found: str) -> FlaggedItem:
        return {
            "id": rule["id"],
            "category": rule["category"],
            "trigger_words": rule["trigger_words"],
            "found_word": found,
            "severity": rule["severity"],
            "legal_basis": rule["legal_basis"],
            "suggestion": rule["suggestion"]
        }

    def scan_image(self, image_input: Union[str, Any], check_logo: bool = True) -> Dict[str, Any]:
        """
        Extracts text from an image and scans it.
        
        Args:
            image_input: PIL Image or path to image file.
            check_logo: Whether to check for Equal Housing Opportunity logo.
            
        Returns:
            Dict with extracted_text, report, and logo_detection results.
        """
        if not HAS_OCR:
            logger.error("OCR dependencies missing.")
            raise ImportError("OCR dependencies (pytesseract, Pillow) are missing.")

        try:
            image = Image.open(image_input)
            extracted_text = pytesseract.image_to_string(image)
            report = self.scan_text(extracted_text)
            
            result = {
                "extracted_text": extracted_text,
                "report": report
            }
            
            # Logo detection
            if check_logo:
                try:
                    from .logo_detector import LogoDetector
                    detector = LogoDetector()
                    logo_result = detector.detect_logo_multi_scale(image)
                    result["logo_detection"] = logo_result
                    
                    # Add warning to report if logo not found
                    if not logo_result.get("found", False):
                        logger.warning("Equal Housing Opportunity logo not detected in image")
                except Exception as e:
                    logger.warning("Logo detection skipped: %s", e)
                    result["logo_detection"] = {"found": False, "message": f"Detection unavailable: {e}"}
            
            return result
        except Exception as e:
            logger.error("Image scan failed: %s", e)
            raise RuntimeError(f"Failed to process image: {str(e)}") from e
