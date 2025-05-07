from langdetect import detect, LangDetectException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LanguageDetector class is used to detect the language of a given text.
# It uses langdetect library which is a port of Google's language detection library.
# The class provides a single method `detect_language` which takes a text as input
# and returns a dictionary with the detected language code and name.
# If the detection fails, it returns None.
class LanguageDetector:
    def __init__(self):
        # ISO 639-1 language codes and names
        self.language_names = {
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
        
        # Special handling for Chinese variants
        self.chinese_map = {
            'zh': 'zh-cn',  # Default Chinese to Simplified
            'zh-cn': 'zh-cn',
            'zh-tw': 'zh-tw'
        }
    
        # Maps a language code to its ISO 639-1 code and name.
        # For example, if the input language code is 'zh', it will be mapped
        # to 'zh-cn' and the name will be 'Chinese (Simplified)'.
        # If the input language code is not found in the mapping, it will
        # return the original language code and name.
    def detect_language(self, text):
        """
        Detect language of provided text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Detected language info or None if detection failed
        """
        if not text or len(text.strip()) < 3:
            return None
            
        try:
            # Detect language
            lang_code = detect(text)
            
            # Handle Chinese variants
            if lang_code.startswith('zh'):
                lang_code = self.chinese_map.get(lang_code, 'zh-cn')
                
            # Default to English if language is unknown
            lang_name = self.language_names.get(lang_code, 'English')
            
            return {
                'code': lang_code,
                'name': lang_name
            }
        except LangDetectException as e:
            logger.error(f"Language detection error: {str(e)}")
            return None
