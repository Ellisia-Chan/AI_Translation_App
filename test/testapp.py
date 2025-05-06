import tkinter as tk
from tkinter import ttk, Canvas, scrolledtext
from PIL import Image, ImageTk

class AITranslatorApp:
    def __init__(self, root):
        self.root = root
        self.configure_window()
        self.setup_assets_path()
        self.create_canvas()
        self.create_ui_elements()
        
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
        
        self.canvas.create_window(50, 180, window=self.lang_select_left_frame, anchor="nw")
        self.canvas.create_window(700, 180, window=self.lang_select_right_frame, anchor="nw")
        
        self.canvas.create_window(50, 250, window=self.lang_source_frame, anchor="nw")
        self.canvas.create_window(700, 250, window=self.lang_target_frame, anchor="nw")
        
        self.canvas.create_window(575, 400, window=self.swap_frame, anchor="nw")
        self.canvas.create_window(525, 650, window=self.translate_frame, anchor="nw")
        
        

        
    def create_buttons(self):
        # sound button
        self.left_lang_sound_btn = tk.Button(self.lang_select_left_frame, image=self.sound_button_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.left_lang_sound_btn.image = self.button_img_tk
        
        self.right_lang_sound_btn = tk.Button(self.lang_select_right_frame, image=self.sound_button_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.right_lang_sound_btn.image = self.button_img_tk
        
        # language selection combobox
        self.left_lang_select_cbx = ttk.Combobox(self.lang_select_left_frame, state="readonly", width=20, font=("Arial", 12))
        self.right_lang_select_cbx = ttk.Combobox(self.lang_select_right_frame, state="readonly", width=20, font=("Arial", 12))
        
        # swap button
        self.swap_btn = tk.Button(self.swap_frame, image=self.btn_swap_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.swap_btn.image = self.button_img_tk
        
        # translate button
        self.translate_btn = tk.Button(self.translate_frame, image=self.translate_btn_img_tk, bg="#D9D9D9", highlightthickness=0, bd=0)
        self.translate_btn.image = self.button_img_tk
        
        
        self.left_lang_select_cbx.grid(row=0, column=1, padx=10)
        self.left_lang_sound_btn.grid(row=0, column=2, padx=10)
        
        self.right_lang_select_cbx.grid(row=0, column=1, padx=10)
        self.right_lang_sound_btn.grid(row=0, column=2, padx=10)
        
        self.swap_btn.grid(row=0, column=0, padx=10)
        self.translate_btn.grid(row=0, column=0, padx=10)
        
        
    def create_text_elements(self):
        # language label
        self.left_lang_detect_lbl = tk.Label(self.lang_select_left_frame, text="English", height=1, width=15, font=("Arial", 12, "bold"))
        self.right_lang_detect_lbl = tk.Label(self.lang_select_right_frame, text="English", height=1, width=15, font=("Arial", 12, "bold"))
        
        self.left_lang_detect_lbl.grid(row=0, column=0, padx=10)
        self.right_lang_detect_lbl.grid(row=0, column=0, padx=10)
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = AITranslatorApp(root)
    root.mainloop()