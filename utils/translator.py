"""
Translation Module
Handles translation between English and Hinglish for AI responses.
"""

from typing import Optional, Dict, Any
from core.ai.base_llm import BaseLLMClient
from core.ai.groq_client import TranslationService


class Translator:
    """
    Translate AI responses between English and Hinglish.
    """
    
    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        """
        Initialize translator.
        
        Args:
            llm_client: Optional LLM client instance.
        """
        self.llm_client = llm_client
        if self.llm_client:
            self.translation_service = TranslationService(self.llm_client)
        else:
            self.translation_service = None
        
        # Common translations cache
        self.translation_cache = {}
    
    def translate_analysis(
        self,
        analysis_data: Dict[str, Any],
        target_language: str = 'english'
    ) -> Dict[str, Any]:
        """
        Translate analysis results to target language.
        
        Args:
            analysis_data: Analysis data dictionary.
            target_language: Target language ('english' or 'hinglish').
            
        Returns:
            Translated analysis data.
        """
        if target_language == 'english':
            return analysis_data
        
        if target_language != 'hinglish':
            raise ValueError(f"Unsupported language: {target_language}")
        
        # Translate key fields
        translated_data = self._translate_dict(analysis_data)
        
        return translated_data
    
    def _translate_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively translate dictionary values.
        
        Args:
            data: Dictionary to translate.
            
        Returns:
            Translated dictionary.
        """
        translated = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Translate string values
                translated[key] = self._translate_text(value)
            elif isinstance(value, dict):
                # Recursively translate nested dictionaries
                translated[key] = self._translate_dict(value)
            elif isinstance(value, list):
                # Translate list items
                translated[key] = self._translate_list(value)
            else:
                # Keep other types as is
                translated[key] = value
        
        return translated
    
    def _translate_list(self, data: list) -> list:
        """
        Translate list items.
        
        Args:
            data: List to translate.
            
        Returns:
            Translated list.
        """
        translated = []
        
        for item in data:
            if isinstance(item, str):
                translated.append(self._translate_text(item))
            elif isinstance(item, dict):
                translated.append(self._translate_dict(item))
            elif isinstance(item, list):
                translated.append(self._translate_list(item))
            else:
                translated.append(item)
        
        return translated
    
    def _translate_text(self, text: str) -> str:
        """
        Translate text to Hinglish.
        
        Args:
            text: Text to translate.
            
        Returns:
            Translated text.
        """
        # Check cache first
        cache_key = f"{text[:100]}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        # Skip very short texts or technical terms
        if len(text) < 5 or self._is_technical_term(text):
            return text
        
        try:
            translated = self.translation_service.translate_to_hinglish(text)
            self.translation_cache[cache_key] = translated
            return translated
        except Exception:
            # Fallback to original text if translation fails
            return text
    
    def _is_technical_term(self, text: str) -> bool:
        """
        Check if text is a technical term that shouldn't be translated.
        
        Args:
            text: Text to check.
            
        Returns:
            True if text is a technical term.
        """
        technical_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'node',
            'aws', 'azure', 'docker', 'kubernetes', 'sql', 'nosql',
            'api', 'rest', 'graphql', 'json', 'xml', 'html', 'css',
            'git', 'github', 'ci/cd', 'devops', 'agile', 'scrum',
            'machine learning', 'ai', 'data science', 'nlp', 'cv',
            'ats', 'resume', 'cv', 'pdf', 'docx', 'ocr'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in technical_keywords)
    
    def translate_response(
        self,
        response_text: str,
        target_language: str = 'english'
    ) -> str:
        """
        Translate a response text.
        
        Args:
            response_text: Text to translate.
            target_language: Target language.
            
        Returns:
            Translated text.
        """
        if target_language == 'english':
            return response_text
        
        if target_language == 'hinglish':
            try:
                return self.translation_service.translate_to_hinglish(response_text)
            except Exception:
                return response_text
        
        raise ValueError(f"Unsupported language: {target_language}")
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages.
        
        Returns:
            List of supported language codes.
        """
        return ['english', 'hinglish']
    
    def is_language_supported(self, language: str) -> bool:
        """
        Check if a language is supported.
        
        Args:
            language: Language code to check.
            
        Returns:
            True if language is supported.
        """
        return language.lower() in self.get_supported_languages()


class HinglishFormatter:
    """
    Format text specifically for Hinglish output.
    """
    
    @staticmethod
    def format_for_hinglish(text: str) -> str:
        """
        Format English text for better Hinglish translation.
        
        Args:
            text: English text to format.
            
        Returns:
            Formatted text.
        """
        # Add context markers for better translation
        formatted = text
        
        # Add section markers
        formatted = formatted.replace('\n\n', '\n\n---SECTION---\n\n')
        
        return formatted
    
    @staticmethod
    def add_hinglish_flavor(text: str) -> str:
        """
        Add Hinglish conversational elements to text.
        
        Args:
            text: Text to enhance.
            
        Returns:
            Enhanced text with Hinglish flavor.
        """
        # This is a simple enhancement - real translation should use AI
        enhancements = {
            'strengths': 'strengths (ye aapki strong points hain)',
            'weaknesses': 'weaknesses (ye improve karne ki zarurat hai)',
            'recommendations': 'recommendations (ye follow karein)',
            'suggestions': 'suggestions (ye try karein)',
        }
        
        for english, hinglish in enhancements.items():
            text = text.replace(english, hinglish)
        
        return text


class LanguageDetector:
    """
    Detect the language of input text.
    """
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect if text is English or Hinglish.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Detected language ('english' or 'hinglish').
        """
        # Simple heuristic detection
        hinglish_indicators = [
            'hai', 'hain', 'ki', 'ka', 'ke', 'ko', 'mein', 'par',
            'aur', 'ya', 'lekin', 'to', 'hi', 'bhi', 'nahi', 'na'
        ]
        
        text_lower = text.lower()
        hinglish_count = sum(1 for indicator in hinglish_indicators if indicator in text_lower)
        
        # If more than 2 Hinglish indicators found, classify as Hinglish
        if hinglish_count >= 2:
            return 'hinglish'
        
        return 'english'
    
    @staticmethod
    def get_confidence(text: str) -> float:
        """
        Get confidence score for language detection.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Confidence score between 0 and 1.
        """
        hinglish_indicators = [
            'hai', 'hain', 'ki', 'ka', 'ke', 'ko', 'mein', 'par',
            'aur', 'ya', 'lekin', 'to', 'hi', 'bhi', 'nahi', 'na'
        ]
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        hinglish_count = sum(1 for indicator in hinglish_indicators if indicator in text_lower)
        
        # Higher confidence with more indicators
        confidence = min(1.0, hinglish_count / 5.0)
        
        return confidence
