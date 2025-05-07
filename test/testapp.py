import tkinter as tk
from tkinter import ttk, Canvas, scrolledtext
from PIL import Image, ImageTk
import sys
import os
import threading
import time

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import translator, language_detector, text_to_speech

class AITranslatorApp:
    def __init__(self, root):
        # Variables
        self.detected_language = tk.StringVar(value="Detecting language...")
        self.languages = translator.get_languages()
        self.language_options = list(self.languages.items())
        self.last_detected_code = None
        self.typing_timer = None
        self.status_var = tk.StringVar(value="Ready")
        
        self.root = root
        self.configure_window()
        self.setup_assets_path()
        self.create_canvas()
        self.create_ui_elements()
        self.Start_Functionality()
        
        
    def configure_window(self):
        """Configure the main window properties"""
        self.root.geometry("1200x800")
        self.root.configure(bg="#F0F0F0")
        self.root.resizable(False, False)
        self.root.title("Language Translator")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def setup_assets_path(self):
        self.bg_img = Image.open("img/frame_1.png")
        self.bg_img = self.bg_img.resize((1200, 800))
        
        self.btn_swap_img = Image.open("img/btn_swap.png")
        self.btn_swap_img = self.btn_swap_img.resize((50, 50))
        self.btn_swap_img_tk = ImageTk.PhotoImage(self.btn_swap_img)
        
        self.button_img = Image.open("img/button.png")
        self.button_img = self.button_img.resize((50, 50))
        self.button_img_tk = ImageTk.PhotoImage(self.button_img)
        
        self.sound_button_img = Image.open("img/sound_button.png")
        self.sound_button_img = self.sound_button_img.resize((50, 50))
        self.sound_button_img_tk = ImageTk.PhotoImage(self.sound_button_img)
        
        self.text_field_img = Image.open("img/text_field.png")
        self.text_field_img = self.text_field_img.resize((450, 400))
        self.text_field_img_tk = ImageTk.PhotoImage(self.text_field_img)
        
        self.translate_btn_img = Image.open("img/translate_btn.png")
        self.translate_btn_img = self.translate_btn_img.resize((150, 50))
        self.translate_btn_img_tk = ImageTk.PhotoImage(self.translate_btn_img)
        
    def create_canvas(self):
        self.canvas = Canvas(
            self.root,
            bg="#F0F0F0",
            height=720,
            width=1080,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
    def create_ui_elements(self):
        """Create all UI elements"""
        self.load_images()
        self.create_frame()
        self.create_buttons()
        self.create_text_elements()
        # self.create_panels()
        
    def load_images(self):
        tk_bg_image = ImageTk.PhotoImage(self.bg_img)
        bg_lbl = tk.Label(self.canvas, image=tk_bg_image)
        bg_lbl.image = tk_bg_image
        bg_lbl.pack()
        
    def create_frame(self):
        # select lang frame
        self.lang_select_left_frame = tk.Frame(self.canvas, width=400, height=50)
        self.lang_select_right_frame = tk.Frame(self.canvas, width=400, height=50)
        
        # language input frame
        self.lang_source_frame = tk.Frame(self.canvas, bg="#D9D9D9", width=450, height=400)
        self.lang_target_frame = tk.Frame(self.canvas, bg="#D9D9D9", width=450, height=400)
        
        # swap and translate frame
        self.swap_frame = tk.Frame(self.canvas, width=50, height=50)
        self.translate_frame = tk.Frame(self.canvas, width=100, height=50)
        
        self.canvas.create_window(150, 180, window=self.lang_select_left_frame, anchor="nw")
        self.canvas.create_window(780, 180, window=self.lang_select_right_frame, anchor="nw")
        
        self.canvas.create_window(50, 250, window=self.lang_source_frame, anchor="nw")
        self.canvas.create_window(700, 250, window=self.lang_target_frame, anchor="nw")
        
        self.canvas.create_window(575, 400, window=self.swap_frame, anchor="nw")
        self.canvas.create_window(525, 650, window=self.translate_frame, anchor="nw")
        
        

        
    def create_buttons(self):
        # sound button
        self.left_lang_sound_btn = tk.Button(self.lang_select_left_frame, image=self.sound_button_img_tk,
                                             highlightthickness=0, bd=0)
        self.left_lang_sound_btn.image = self.button_img_tk
        
        self.right_lang_sound_btn = tk.Button(self.lang_select_right_frame, image=self.sound_button_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.right_lang_sound_btn.image = self.button_img_tk
        
        # language selection combobox
        self.right_lang_select_cbx = ttk.Combobox(self.lang_select_right_frame, state="readonly", width=20, font=("Arial", 14))
        
        # swap button
        self.swap_btn = tk.Button(self.swap_frame, image=self.btn_swap_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.swap_btn.image = self.button_img_tk
        
        # translate button
        self.translate_btn = tk.Button(self.translate_frame, image=self.translate_btn_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.translate_btn.image = self.button_img_tk
        
        self.left_lang_sound_btn.grid(row=0, column=2, padx=50)
        
        self.right_lang_select_cbx.grid(row=0, column=1, padx=10)
        self.right_lang_sound_btn.grid(row=0, column=2, padx=10)
        
        self.swap_btn.grid(row=0, column=0, padx=10)
        self.translate_btn.grid(row=0, column=0, padx=10)
        
        
    def create_text_elements(self):
        # language label
        self.left_lang_detect_lbl = tk.Label(self.lang_select_left_frame, text="English", height=1, width=18, font=("Arial", 16, "bold"))
        
        self.left_lang_detect_lbl.grid(row=0, column=0, padx=10)
        
        # Text field
        self.source_text = tk.Text(
            self.lang_source_frame, 
            width=30,
            height=10, 
            wrap=tk.WORD,
            font=('Arial', 20),
            borderwidth=1,
            relief=tk.SOLID
        )
        self.source_text.grid(row=0, column=0, padx=10, pady=10)
        
        self.target_text = tk.Text(
            self.lang_target_frame, 
            width=30,
            height=10, 
            wrap=tk.WORD,
            font=('Arial', 20),
            borderwidth=1,
            relief=tk.SOLID
        )
        self.target_text.grid(row=0, column=0, padx=10, pady=10)
        
    def Start_Functionality(self):
        """Connect UI elements to their functionality"""
        # Set up language comboboxes
        language_names = [name for _, name in self.language_options]
        language_codes = [code for code, _ in self.language_options]
        
        # Configure target language combobox
        self.right_lang_select_cbx["values"] = language_names
        
        # Set default to English
        english_index = language_codes.index("en") if "en" in language_codes else 0
        self.right_lang_select_cbx.current(english_index)
        
        # Store reference to target language combobox for translation functions
        self.target_language = self.right_lang_select_cbx
        
        # Bind events
        self.source_text.bind("<KeyRelease>", self.on_source_text_change)
        self.right_lang_select_cbx.bind("<<ComboboxSelected>>", lambda e: self.handle_translation())
        
        # Connect buttons to functions
        self.swap_btn.config(command=self.handle_swap_languages)
        self.translate_btn.config(command=self.handle_translation)
        
        # Connect audio buttons
        self.left_lang_sound_btn.config(
            command=lambda: self.handle_speak_text(self.source_text.get("1.0", tk.END), self.last_detected_code)
        )
        self.right_lang_sound_btn.config(
            command=lambda: self.handle_speak_text(
                self.target_text.get("1.0", tk.END), 
                language_codes[self.right_lang_select_cbx.current()]
            )
        )
        
        # Update language label binding
        self.detected_language.trace_add("write", 
            lambda *args: self.left_lang_detect_lbl.config(text=self.detected_language.get())
        )
        
        # Add status bar at the bottom of the window
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            padding=(10, 2)
        )
        status_bar.grid(row=1, column=0, sticky="ew")
        
        # Initialize language detection
        self.detect_language()
    
    # ==========================================================================
    # Functions
    # ==========================================================================
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

if __name__ == "__main__":
    root = tk.Tk()
    app = AITranslatorApp(root)
    root.mainloop()