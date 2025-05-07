from gtts import gTTS
import pygame
import io
import tempfile
import os
import logging
import time
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The TextToSpeech class handles text-to-speech conversion using gTTS and plays the audio using pygame.
# It manages temporary audio files and provides functionality to stop currently playing audio.
class TextToSpeech:
    def __init__(self):
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        self.is_playing = False
        self.temp_files = []
    
    def __del__(self):
        # Clean up temporary files when object is destroyed
        self.cleanup_temp_files()
        
    def cleanup_temp_files(self):
        """Remove temporary audio files"""
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.error(f"Failed to delete temporary file {file_path}: {str(e)}")
        self.temp_files = []
        
    def stop_audio(self):
        """Stop any currently playing audio"""
        if pygame.mixer.get_busy():
            pygame.mixer.music.stop()
        self.is_playing = False
        
    def text_to_speech_memory(self, text, lang='en'):
        """
        Convert text to speech and play it directly from memory
        
        Args:
            text (str): Text to convert to speech
            lang (str): Language code for TTS
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text.strip():
            logger.warning("Empty text provided for TTS")
            return False
            
        try:
            # Stop any currently playing audio
            self.stop_audio()
            
            # Create gTTS object
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Save to in-memory file-like object
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(mp3_fp.read())
                temp_path = temp_file.name
                
            # Keep track of the temporary file to delete it later
            self.temp_files.append(temp_path)
            
            # Play the audio
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            self.is_playing = True
            
            # Start a thread to monitor when playback ends
            def check_if_playing():
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                self.is_playing = False
                
            threading.Thread(target=check_if_playing, daemon=True).start()
            
            return True
            
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            return False