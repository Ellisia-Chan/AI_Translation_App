import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
from pathlib import Path



class TranslatorApp:
    """Main application class for the language translator UI"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.configure_window()
        self.setup_assets_path()
        self.create_canvas()
        self.create_ui_elements()
        
    def configure_window(self):
        """Configure the main window properties"""
        self.root.geometry("1440x1024")
        self.root.configure(bg="#F0F0F0")
        self.root.resizable(True, True)
        self.root.title("Language Translator")
        
    def setup_assets_path(self):
        """Set up the assets path"""
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "assets"
        
    def relative_to_assets(self, path):
        """Convert relative path to absolute asset path"""
        return self.assets_path / path
        
    def create_canvas(self):
        """Create the main canvas"""
        self.canvas = Canvas(
            self.root,
            bg="#F0F0F0",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
    def create_ui_elements(self):
        """Create all UI elements"""
        self.load_images()
        self.create_buttons()
        self.create_text_elements()
        self.create_panels()
        
    def load_images(self):
        """Load all images used in the application"""
        # Store images as attributes to prevent garbage collection
        self.images = {}
        
        # Background and decorative images
        image_files = [
            "flower_1.png", "flower_2.png", "flower_3.png", 
            "flower_4.png", "img_title.png", "img_targetLang.png",
            "image_7.png", "img_detectedLang.png", "image_9.png", "image_10.png"
        ]
        
        for i, file in enumerate(image_files, 1):
            try:
                self.images[f"image_{i}"] = PhotoImage(file=self.relative_to_assets(file))
            except tk.TclError:
                print(f"Warning: Could not load {file}")
        
        # Button images
        button_files = ["btn_swap.png", "btn_leftSpeaker.png", "btn_rightSpeaker.png", "btn_translate.png"]
        
        for i, file in enumerate(button_files, 1):
            try:
                self.images[f"button_{i}"] = PhotoImage(file=self.relative_to_assets(file))
            except tk.TclError:
                print(f"Warning: Could not load {file}")
        
        # Place images on canvas
        self.place_images()
        
    def place_images(self):
        """Place all images on the canvas"""
        # Main images
        image_positions = [
             (1335, 764),
            (705, 764),
            (564, 1012),
            (1264, 1036),
            (720, 128),
            (938, 232),
            (1174, 232),
            (159, 232),
            (406, 232),
            (336, 552)
        ]
        
        for i, pos in enumerate(image_positions, 1):
            img_key = f"image_{i}"
            if img_key in self.images:
                self.canvas.create_image(pos[0], pos[1], image=self.images[img_key])
    
    def create_buttons(self):
        """Create all buttons"""
        # Translate button (center)
        self.translate_button = Button(
            image=self.images.get("btn_swap"),
            borderwidth=0,
            highlightthickness=0,
            command=self.on_translate_click,
            relief="flat"
        )
        self.translate_button.place(x=680.0, y=480.0, width=80.0, height=80.0)
        
        # Right language selection button
        self.right_lang_button = Button(
            image=self.images.get("btn_leftSpeaker"),
            borderwidth=0,
            highlightthickness=0,
            command=self.on_right_lang_click,
            relief="flat"
        )
        self.right_lang_button.place(x=1336.0, y=208.0, width=48.0, height=48.0)
        
        # Left language selection button
        self.left_lang_button = Button(
            image=self.images.get("btn_rightSpeaker"),
            borderwidth=0,
            highlightthickness=0,
            command=self.on_left_lang_click,
            relief="flat"
        )
        self.left_lang_button.place(x=568.0, y=208.0, width=48.0, height=48.0)
        
        # Bottom action button
        self.action_button = Button(
            image=self.images.get("btn_translate"),
            borderwidth=0,
            highlightthickness=0,
            command=self.on_action_click,
            relief="flat"
        )
        self.action_button.place(x=616.0, y=880.0, width=208.0, height=59.0)
    
    def create_text_elements(self):
        """Create text elements on canvas"""
        # Right side language label
        self.canvas.create_text(
            1029.0, 208.0,
            anchor="nw",
            text="Detected Language",
            fill="#000000",
            font=("PlayfairDisplay Regular", 20 * -1)
        )
        
        # Left side language label
        self.canvas.create_text(
            261.0, 208.0,
            anchor="nw",
            text="Detected Language",
            fill="#000000",
            font=("PlayfairDisplay Regular", 20 * -1)
        )
    
    def create_panels(self):
        """Create panel areas"""
        # Output text panel
        self.canvas.create_rectangle(
            824.0, 272.0,
            1384.0, 832.0,
            fill="#D9D9D9",
            outline=""
        )
    
    # Button click handlers
    def on_translate_click(self):
        """Handle translate button click"""
        print("Translate button clicked")
        # Implement translation logic here
        
    def on_right_lang_click(self):
        """Handle right language button click"""
        print("Right language button clicked")
        # Implement language selection logic here
        
    def on_left_lang_click(self):
        """Handle left language button click"""
        print("Left language button clicked")
        # Implement language selection logic here
        
    def on_action_click(self):
        """Handle bottom action button click"""
        print("Action button clicked")
        # Implement action logic here


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()