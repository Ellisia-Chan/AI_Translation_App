from googletrans import Translator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        # Languages supported by the translator
        self.languages = {
            'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
            'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
            'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
            'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
            'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
            'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
            'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian',
            'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
            'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi',
            'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo',
            'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
            'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer',
            'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao',
            'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
            'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
            'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian',
            'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 'ps': 'Pashto',
            'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
            'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic',
            'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi',
            'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali',
            'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish',
            'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish',
            'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese',
            'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba',
            'zu': 'Zulu'
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