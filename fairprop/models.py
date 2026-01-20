import logging
import uuid


# Configure logging
logger = logging.getLogger("fairprop.models")

class ModelManager:
    """
    Singleton-like manager for lazy loading of heavy AI models.
    This prevents the CLI from being slow on startup if AI features aren't used.
    """
    _instance = None
    
    def __init__(self):
        self._sentence_transformer = None
        self._chroma_client = None
        self._chroma_collection = None
        self._fixer_pipeline = None
        self._guardrail_pipeline = None
        self._has_ai = False
        self._check_environment()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _check_environment(self):
        """Checks if necessary packages are installed."""
        try:
            import torch
            import transformers
            import chromadb
            import sentence_transformers
            # Pylint: disable unused import warning by acknowledging check
            _ = (torch, transformers, chromadb, sentence_transformers)
            self._has_ai = True
        except ImportError as e:
            logger.warning("AI dependencies missing: %s. Running in rule-only mode.", e)
            self._has_ai = False

    @property
    def has_ai(self) -> bool:
        return self._has_ai

    @property
    def sentence_transformer(self):
        if not self._has_ai: return None
        if self._sentence_transformer is None:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading SentenceTransformer model...")
            self._sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        return self._sentence_transformer

    @property
    def chroma_client(self):
        if not self._has_ai: return None
        if self._chroma_client is None:
            import chromadb
            logger.info("Initializing ChromaDB client...")
            self._chroma_client = chromadb.Client()
        return self._chroma_client

    def reset_collection(self):
        """Reset the vector database collection."""
        self._chroma_collection = None

    def get_collection(self, rules: list):
        """Gets or creates the ChromaDB collection for rules."""
        if not self._has_ai: return None
        if self._chroma_collection is None:
            client = self.chroma_client
            collection_name = f"fha_rules_{uuid.uuid4().hex[:8]}"
            self._chroma_collection = client.create_collection(name=collection_name)
            self._index_rules(rules)
        return self._chroma_collection

    def _index_rules(self, rules: list):
        """Indexes rules into the vector DB."""
        if not self._has_ai: return
        
        documents = []
        metadatas = []
        ids = []

        for rule in rules:
            for trigger in rule.get("trigger_words", []):
                documents.append(trigger)
                metadatas.append({
                    "rule_id": rule["id"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "trigger": trigger
                })
                ids.append(str(uuid.uuid4()))
        
        if documents:
            self._chroma_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info("Indexed %d trigger variants into Vector DB.", len(documents))

    @property
    def fixer_pipeline(self):
        if not self._has_ai: return None
        if self._fixer_pipeline is None:
            from transformers import pipeline
            logger.info("Loading Generator model (flan-t5-small)...")
            try:
                self._fixer_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")
            except Exception as e:
                logger.error("Failed to load fixer model: %s", e)
                return None
        return self._fixer_pipeline

    @property
    def guardrail_pipeline(self):
        if not self._has_ai: return None
        if self._guardrail_pipeline is None:
            from transformers import pipeline
            logger.info("Loading Neural Guardrail (Zero-Shot based on facebook/bart-large-mnli)...")
            try:
                self._guardrail_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            except Exception as e:
                logger.error("Failed to load guardrail model: %s", e)
                return None
        return self._guardrail_pipeline
