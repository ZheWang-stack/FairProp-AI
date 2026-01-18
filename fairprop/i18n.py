"""
Internationalization (i18n) module for FairProp.
Supports multi-language translations for rules, suggestions, and UI messages.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger("fairprop.i18n")

class I18n:
    """
    Internationalization handler for FairProp.
    Supports dynamic language switching and translation of rules/messages.
    """
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Español (Spanish)',
        'pt': 'Português (Portuguese)',
        'fr': 'Français (French)',
        'de': 'Deutsch (German)',
        'nl': 'Nederlands (Dutch)',
        'zh': '中文 (Chinese)',
        'ja': '日本語 (Japanese)',
        'ko': '한국어 (Korean)'
    }
    
    def __init__(self, language: str = 'en', translations_dir: str = 'translations'):
        """
        Initialize i18n handler.
        
        Args:
            language: Language code (ISO 639-1), default 'en'
            translations_dir: Directory containing translation files
        """
        self.language = language
        self.translations_dir = Path(translations_dir)
        self.translations = {}
        self._load_translations()
    
    def _load_translations(self):
        """Load translation file for current language."""
        translation_file = self.translations_dir / f"{self.language}.json"
        
        if translation_file.exists():
            try:
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                logger.info(f"Loaded translations for language: {self.language}")
            except Exception as e:
                logger.warning(f"Failed to load translations for {self.language}: {e}")
                self.translations = {}
        else:
            logger.warning(f"Translation file not found for {self.language}, using English defaults")
            self.translations = {}
    
    def t(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """
        Translate a key to the current language.
        
        Args:
            key: Translation key (dot notation supported, e.g., 'ui.scan_button')
            default: Default text if translation not found
            **kwargs: Variables for string formatting
            
        Returns:
            Translated string or default
        """
        # Support nested keys with dot notation
        keys = key.split('.')
        value = self.translations
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                value = default or key
                break
        
        # Format with variables if provided
        if isinstance(value, str) and kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing variable in translation: {e}")
        
        return value
    
    def translate_rule(self, rule: Dict) -> Dict:
        """
        Translate a rule's category, legal_basis, and suggestion.
        
        Args:
            rule: Rule dictionary
            
        Returns:
            Translated rule dictionary
        """
        translated_rule = rule.copy()
        
        # Try to translate category
        category_key = f"categories.{rule.get('category', '').lower().replace(' ', '_')}"
        translated_rule['category'] = self.t(category_key, default=rule.get('category'))
        
        # Try to translate suggestion
        suggestion_key = f"suggestions.{rule.get('id', '')}"
        translated_rule['suggestion'] = self.t(suggestion_key, default=rule.get('suggestion'))
        
        return translated_rule
    
    def get_ui_messages(self) -> Dict[str, str]:
        """
        Get all UI messages for current language.
        
        Returns:
            Dictionary of UI messages
        """
        return self.translations.get('ui', {})
    
    def set_language(self, language: str):
        """
        Change the current language.
        
        Args:
            language: New language code
        """
        if language in self.SUPPORTED_LANGUAGES:
            self.language = language
            self._load_translations()
            logger.info(f"Language changed to: {self.SUPPORTED_LANGUAGES[language]}")
        else:
            logger.warning(f"Unsupported language: {language}")
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """Get dictionary of supported language codes and names."""
        return cls.SUPPORTED_LANGUAGES.copy()


# Global i18n instance
_i18n_instance = None

def get_i18n(language: str = 'en') -> I18n:
    """Get or create global i18n instance."""
    global _i18n_instance
    if _i18n_instance is None or _i18n_instance.language != language:
        _i18n_instance = I18n(language)
    return _i18n_instance

def t(key: str, default: Optional[str] = None, **kwargs) -> str:
    """Shorthand for translation."""
    return get_i18n().t(key, default, **kwargs)
