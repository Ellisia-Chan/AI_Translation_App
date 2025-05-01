import tkinter as tk
from tkinter import ttk
import threading
import time

class AITranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Translator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")
        
        # Set app icon and styling
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        self.style.configure("Header.TLabel", background="#f5f5f5", font=("Arial", 12, "bold"))
        
        # Available languages
        self.languages = [
            "English", "Spanish", "French", "German", "Italian", 
            "Portuguese", "Russian", "Japanese", "Chinese", "Korean",
            "Arabic", "Hindi", "Dutch", "Swedish", "Greek"
        ]
        
        # Default values
        self.source_language = "Auto-detect"
        self.target_language = "English"
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source container
        source_frame = ttk.Frame(main_frame)
        source_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        source_header_frame = ttk.Frame(source_frame)
        source_header_frame.pack(fill=tk.X)
        
        self.source_lang_label = ttk.Label(source_header_frame, text="Detected: Auto-detect", style="Header.TLabel")
        self.source_lang_label.pack(side=tk.LEFT, pady=5)
        
        self.source_listen_btn = ttk.Button(source_header_frame, text="🔊 Listen", command=self.listen_source)
        self.source_listen_btn.pack(side=tk.RIGHT, pady=5)
        
        self.source_text = tk.Text(source_frame, height=10, width=80, font=("Arial", 11))
        self.source_text.pack(fill=tk.BOTH, expand=True)
        self.source_text.bind("<KeyRelease>", self.on_source_text_change)
        
        # Middle controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        self.swap_btn = ttk.Button(controls_frame, text="⇅ Swap", command=self.swap_languages)
        self.swap_btn.pack(side=tk.LEFT, padx=5)
        
        self.translate_btn = ttk.Button(controls_frame, text="Translate", command=self.translate)
        self.translate_btn.pack(side=tk.RIGHT, padx=5)
        
        # Target container
        target_frame = ttk.Frame(main_frame)
        target_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        target_header_frame = ttk.Frame(target_frame)
        target_header_frame.pack(fill=tk.X)
        
        self.target_lang_var = tk.StringVar(value="English")
        self.target_lang_combo = ttk.Combobox(target_header_frame, textvariable=self.target_lang_var, values=self.languages, state="readonly")
        self.target_lang_combo.pack(side=tk.LEFT, pady=5)
        self.target_lang_combo.bind("<<ComboboxSelected>>", self.on_target_language_change)
        
        self.target_listen_btn = ttk.Button(target_header_frame, text="🔊 Listen", command=self.listen_target)
        self.target_listen_btn.pack(side=tk.RIGHT, pady=5)
        
        self.target_text = tk.Text(target_frame, height=10, width=80, font=("Arial", 11), state="disabled")
        self.target_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def on_source_text_change(self, event=None):
        """Detect language when user types in source text field"""
        text = self.source_text.get("1.0", "end-1c").strip()
        if len(text) > 5:
            # Simulate language detection (would be replaced with actual AI detection)
            self.detect_language()
    
    def detect_language(self):
        """Simulate language detection"""
        self.status_var.set("Detecting language...")
        
        # Simulate processing time
        def detect():
            time.sleep(1)  # Simulate API call
            # This would be replaced with actual language detection logic
            detected = "English"  # Placeholder
            self.source_language = detected
            self.source_lang_label.config(text=f"Detected: {detected}")
            self.status_var.set("Language detected")
            
        threading.Thread(target=detect, daemon=True).start()
    
    def on_target_language_change(self, event=None):
        """Handle target language change"""
        self.target_language = self.target_lang_var.get()
        if self.source_text.get("1.0", "end-1c").strip():
            self.translate()
    
    def swap_languages(self):
        """Swap source and target languages"""
        # Can only swap if source language is not auto-detect
        if self.source_language != "Auto-detect":
            # Swap languages
            temp = self.source_language
            self.source_language = self.target_language
            self.target_language = temp
            
            # Update UI
            self.source_lang_label.config(text=f"Detected: {self.source_language}")
            self.target_lang_var.set(self.target_language)
            
            # Swap text
            source_text = self.source_text.get("1.0", "end-1c")
            
            self.target_text.config(state="normal")
            target_text = self.target_text.get("1.0", "end-1c")
            self.target_text.delete("1.0", "end")
            self.target_text.config(state="disabled")
            
            self.source_text.delete("1.0", "end")
            self.source_text.insert("1.0", target_text)
            
            self.translate()
    
    def translate(self):
        """Translate text from source to target language"""
        text = self.source_text.get("1.0", "end-1c").strip()
        if not text:
            return
        
        self.status_var.set(f"Translating from {self.source_language} to {self.target_language}...")
        
        # Simulate translation process
        def translate_text():
            time.sleep(1.5)  # Simulate API call
            
            # This would be replaced with actual translation logic
            translated_text = f"[Translation of '{text}' from {self.source_language} to {self.target_language}]"
            
            self.target_text.config(state="normal")
            self.target_text.delete("1.0", "end")
            self.target_text.insert("1.0", translated_text)
            self.target_text.config(state="disabled")
            
            self.status_var.set("Translation complete")
            
        threading.Thread(target=translate_text, daemon=True).start()
    
    def listen_source(self):
        """Text-to-speech for source text"""
        text = self.source_text.get("1.0", "end-1c").strip()
        if text:
            self.status_var.set(f"Playing audio for source text...")
            # This would be replaced with actual TTS logic
            
            # Simulate TTS process
            def tts():
                time.sleep(1)  # Simulate API call
                self.status_var.set("Audio playback complete")
                
            threading.Thread(target=tts, daemon=True).start()
    
    def listen_target(self):
        """Text-to-speech for target text"""
        text = self.target_text.get("1.0", "end-1c").strip()
        if text:
            self.status_var.set(f"Playing audio for translated text...")
            # This would be replaced with actual TTS logic
            
            # Simulate TTS process
            def tts():
                time.sleep(1)  # Simulate API call
                self.status_var.set("Audio playback complete")
                
            threading.Thread(target=tts, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AITranslatorApp(root)
    root.mainloop()