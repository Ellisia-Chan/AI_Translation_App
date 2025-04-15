from .translator import TranslationService
from .language_detector import LanguageDetector
from .text_to_speech import TextToSpeech

# Initialize services
translator = TranslationService()
language_detector = LanguageDetector()
text_to_speech = TextToSpeech()

__all__ = ['translator', 'language_detector', 'text_to_speech']
