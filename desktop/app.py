import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os
import threading
import time

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import translator, language_detector, text_to_speech

class ModernUI:
    """Theme and style manager for the application"""
    
    # Color scheme
    PRIMARY = "#1e88e5"      # Main blue
    PRIMARY_DARK = "#005cb2" # Darker blue
    SECONDARY = "#26a69a"    # Teal accent
    BG_LIGHT = "#f5f5f5"     # Light background
    BG_DARK = "#e0e0e0"      # Darker background
    TEXT_PRIMARY = "#212121" # Main text
    TEXT_SECONDARY = "#757575" # Secondary text
    SUCCESS = "#43a047"      # Green
    ERROR = "#e53935"        # Red
    
    # Font sizes
    FONT_LARGE = 12
    FONT_MEDIUM = 11
    FONT_SMALL = 10
    
    @classmethod
    def setup_styles(cls, root):
        """Configure ttk styles for the application"""
        style = ttk.Style(root)
        
        # Try to use a platform-appropriate theme as a base
        try:
            if sys.platform.startswith('win'):
                style.theme_use('vista')
            elif sys.platform.startswith('darwin'):
                style.theme_use('aqua')
            else:
                style.theme_use('clam')
        except tk.TclError:
            # Fall back to default if the theme is not available
            pass
        
        # Configure common elements
        style.configure('TFrame', background=cls.BG_LIGHT)
        style.configure('TLabel', background=cls.BG_LIGHT, foreground=cls.TEXT_PRIMARY, font=(None, cls.FONT_MEDIUM))
        style.configure('TButton', font=(None, cls.FONT_MEDIUM))
        
        # Custom styles
        style.configure('Header.TLabel', font=(None, cls.FONT_LARGE, 'bold'), foreground=cls.PRIMARY_DARK)
        style.configure('Status.TLabel', background=cls.BG_DARK, foreground=cls.TEXT_SECONDARY, font=(None, cls.FONT_SMALL))
        
        # LabelFrame styling
        style.configure('TLabelframe', background=cls.BG_LIGHT)
        style.configure('TLabelframe.Label', background=cls.BG_LIGHT, foreground=cls.PRIMARY_DARK, font=(None, cls.FONT_MEDIUM, 'bold'))
        
        # Button styles
        style.configure('Action.TButton', font=(None, cls.FONT_MEDIUM, 'bold'))
        
        return style

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Translator")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set background color for the root window
        self.root.configure(bg=ModernUI.BG_LIGHT)
        
        # Setup themes and styles
        self.style = ModernUI.setup_styles(root)
        
        # Variables
        self.detected_language = tk.StringVar(value="Detecting language...")
        self.languages = translator.get_languages()
        self.language_options = list(self.languages.items())
        self.last_detected_code = None
        self.typing_timer = None
        self.status_var = tk.StringVar(value="Ready")
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding=15, style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        header_label = ttk.Label(header_frame, text="AI Language Translator", style='Header.TLabel')
        header_label.pack(side=tk.LEFT)
        
        # Top frame for source text
        source_frame = ttk.LabelFrame(main_container, text="Source Text", padding=10)
        source_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Source controls
        source_controls = ttk.Frame(source_frame, style='TFrame')
        source_controls.pack(fill=tk.X, pady=(0, 8))
        
        # Source language indicator with better layout
        lang_frame = ttk.Frame(source_controls, style='TFrame')
        lang_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        lang_label = ttk.Label(lang_frame, text="Detected Language:", style='TLabel')
        lang_label.pack(side=tk.LEFT, padx=(0, 5))
        
        detected_lang_label = ttk.Label(lang_frame, textvariable=self.detected_language, foreground=ModernUI.PRIMARY_DARK, font=(None, ModernUI.FONT_MEDIUM, 'bold'))
        detected_lang_label.pack(side=tk.LEFT)
        
        # Source audio button
        source_audio_btn = ttk.Button(source_controls, text="Listen", width=8, 
                                     command=lambda: self.handle_speak_text(self.source_text.get("1.0", tk.END), self.last_detected_code))
        source_audio_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Source text with improved styling
        self.source_text = scrolledtext.ScrolledText(
            source_frame, 
            height=12, 
            wrap=tk.WORD,
            font=('Arial', 11),
            borderwidth=1,
            relief=tk.SOLID
        )
        self.source_text.pack(fill=tk.BOTH, expand=True)
        self.source_text.bind("<KeyRelease>", self.on_source_text_change)
        
        # Middle controls in a nice frame
        controls_frame = ttk.Frame(main_container, style='TFrame')
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Center the controls
        controls_center = ttk.Frame(controls_frame, style='TFrame')
        controls_center.pack(expand=True)
        
        # Swap button
        swap_btn = ttk.Button(controls_center, text="Swap Languages", style='Action.TButton',
                             command=self.handle_swap_languages)
        swap_btn.pack(side=tk.LEFT, padx=5)
        
        # Translate button
        translate_btn = ttk.Button(controls_center, text="Translate", style='Action.TButton',
                                 command=self.handle_translation)
        translate_btn.pack(side=tk.LEFT, padx=5)
        
        # Bottom frame for target text
        target_frame = ttk.LabelFrame(main_container, text="Translation", padding=10)
        target_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Target controls
        target_controls = ttk.Frame(target_frame, style='TFrame')
        target_controls.pack(fill=tk.X, pady=(0, 8))
        
        # Target language selector with better layout
        lang_select_frame = ttk.Frame(target_controls, style='TFrame')
        lang_select_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        lang_target_label = ttk.Label(lang_select_frame, text="Target Language:", style='TLabel')
        lang_target_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create language dropdown
        self.target_language = ttk.Combobox(lang_select_frame, width=25, state="readonly",
                                          font=('Arial', ModernUI.FONT_MEDIUM))
        self.target_language.pack(side=tk.LEFT)
        
        # Set language options
        language_names = [name for _, name in self.language_options]
        language_codes = [code for code, _ in self.language_options]
        self.target_language["values"] = language_names
        
        # Set default to English
        english_index = language_codes.index("en") if "en" in language_codes else 0
        self.target_language.current(english_index)
        self.target_language.bind("<<ComboboxSelected>>", lambda e: self.handle_translation())
        
        # Target audio button
        target_audio_btn = ttk.Button(target_controls, text="Listen", width=8,
                                     command=lambda: self.handle_speak_text(self.target_text.get("1.0", tk.END), 
                                                                          language_codes[self.target_language.current()]))
        target_audio_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Target text with improved styling
        self.target_text = scrolledtext.ScrolledText(
            target_frame, 
            height=12, 
            wrap=tk.WORD,
            font=('Arial', 11),
            borderwidth=1,
            relief=tk.SOLID
        )
        self.target_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar with professional styling
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            style='Status.TLabel',
            padding=(10, 2)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def on_source_text_change(self, event=None):
        """Handle source text changes with debounce"""
        # Cancel previous timer if it exists
        if self.typing_timer is not None:
            self.root.after_cancel(self.typing_timer)
            
        # Set new timer
        if self.source_text.get("1.0", tk.END).strip():
            self.typing_timer = self.root.after(500, self.detect_language)
        else:
            self.detected_language.set("Detecting language...")
            self.target_text.delete("1.0", tk.END)
    
    def detect_language(self):
        """Detect language of source text"""
        text = self.source_text.get("1.0", tk.END).strip()
        
        if not text:
            self.detected_language.set("Detecting language...")
            return
            
        self.status_var.set("Detecting language...")
        
        # Use threading to avoid blocking UI
        def detect_thread():
            result = language_detector.detect_language(text)
            
            # Update UI from main thread
            self.root.after(0, lambda: self.update_detected_language(result))
            
        threading.Thread(target=detect_thread, daemon=True).start()
    
    def update_detected_language(self, result):
        """Update UI with detected language"""
        if result:
            self.detected_language.set(result["name"])
            self.last_detected_code = result["code"]
            self.status_var.set("Language detected")
            
            # Auto translate
            self.handle_translation()
        else:
            self.detected_language.set("Unknown")
            self.last_detected_code = None
            self.status_var.set("Could not detect language")
    
    def handle_translation(self):
        """Translate the source text"""
        text = self.source_text.get("1.0", tk.END).strip()
        
        if not text:
            self.target_text.delete("1.0", tk.END)
            return
            
        # Get target language code
        language_codes = [code for code, _ in self.language_options]
        target_lang = language_codes[self.target_language.current()]
        
        self.status_var.set("Translating...")
        
        # Use threading to avoid blocking UI
        def translate_thread():
            result = translator.translate_text(
                text=text,
                target_lang=target_lang,
                source_lang=self.last_detected_code
            )
            
            # Update UI from main thread
            self.root.after(0, lambda: self.update_translation(result))
            
        threading.Thread(target=translate_thread, daemon=True).start()
    
    def update_translation(self, result):
        """Update UI with translation result"""
        if result["success"]:
            self.target_text.delete("1.0", tk.END)
            self.target_text.insert("1.0", result["translated_text"])
            self.status_var.set("Translation complete")
        else:
            self.target_text.delete("1.0", tk.END)
            self.target_text.insert("1.0", f"Error: {result['error']}")
            self.status_var.set("Translation failed")
    
    def handle_swap_languages(self):
        """Swap source and target languages"""
        if not self.last_detected_code:
            return
            
        # Swap text
        source_text = self.source_text.get("1.0", tk.END)
        target_text = self.target_text.get("1.0", tk.END)
        
        self.source_text.delete("1.0", tk.END)
        self.source_text.insert("1.0", target_text)
        
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", source_text)
        
        # Set target language to previously detected language
        language_codes = [code for code, _ in self.language_options]
        try:
            new_index = language_codes.index(self.last_detected_code)
            self.target_language.current(new_index)
        except ValueError:
            # Language not found in list
            pass
        
        # Re-detect language
        self.detect_language()
    
    def handle_speak_text(self, text, lang_code):
        """Convert text to speech"""
        text = text.strip()
        if not text or not lang_code:
            return
            
        self.status_var.set("Playing audio...")
        
        # Use threading to avoid blocking UI
        def speak_thread():
            success = text_to_speech.text_to_speech_memory(text, lang_code)
            
            # Update status from main thread
            if success:
                self.root.after(0, lambda: self.status_var.set("Audio playing..."))
                
                # Check periodically if audio has finished
                def check_audio():
                    if not text_to_speech.is_playing:
                        self.status_var.set("Ready")
                    else:
                        self.root.after(100, check_audio)
                
                self.root.after(100, check_audio)
            else:
                self.root.after(0, lambda: self.status_var.set("Audio playback failed"))
                
        threading.Thread(target=speak_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
    
    # Clean up resources
    text_to_speech.cleanup_temp_files()

if __name__ == "__main__":
    main()