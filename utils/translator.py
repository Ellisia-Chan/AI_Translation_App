from googletrans import Translator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        # Languages supported by the translator
        self.languages = {
            'ar': 'Arabic', 'bg': 'Bulgarian',
            'ceb': 'Cebuano', 'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'cs': 'Czech', 'nl': 'Dutch', 'en': 'English',
            'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
            'fr': 'French','de': 'German', 'el': 'Greek',
            'iw': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian',
            'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
            'jw': 'Javanese','ko': 'Korean',
            'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'mn': 'Mongolian',
            'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
            'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
            'ro': 'Romanian', 'ru': 'Russian',
            'sr': 'Serbian', 'sl': 'Slovenian', 'so': 'Somali',
            'es': 'Spanish', 'sv': 'Swedish', 
            'th': 'Thai', 'tr': 'Turkish',
            'uk': 'Ukrainian', 'vi': 'Vietnamese',
        }
    
    def get_languages(self):
        """Return dictionary of available languages"""
        return self.languages
    
    def translate_text(self, text, target_lang='en', source_lang=None):
        """
        Translate text to target language
        
        Args:
            text (str): Text to translate
            target_lang (str): Target language code
            source_lang (str, optional): Source language code. If None, auto-detect
            
        Returns:
            dict: Translation result with text, detected language, and translation
        """
        if not text.strip():
            return {
                'original_text': text,
                'detected_language': None,
                'translated_text': '',
                'success': False,
                'error': 'Empty text'
            }
            
        try:
            # Perform translation
            result = self.translator.translate(
                text,
                dest=target_lang,
                src=source_lang if source_lang else 'auto'
            )
            
            return {
                'original_text': text,
                'detected_language': result.src,
                'detected_language_name': self.languages.get(result.src, 'Unknown'),
                'translated_text': result.text,
                'target_language': target_lang,
                'target_language_name': self.languages.get(target_lang, 'Unknown'),
                'success': True,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                'original_text': text,
                'detected_language': None,
                'translated_text': '',
                'success': False,
                'error': str(e)
            }