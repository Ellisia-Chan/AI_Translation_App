import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("AI Language Translator")
root.geometry("1000x700")
root.configure(bg="#f5f5f5")

# Title
title = tk.Label(root, text="AI Language Translator", font=("Georgia", 24, "bold"), bg="#f5f5f5", fg="black")
title.pack(pady=20)

# Top Frame for language labels
top_frame = tk.Frame(root, bg="#f5f5f5")
top_frame.pack(pady=10)

# Left language info
left_language_label = tk.Label(top_frame, text="Detected Language", font=("Georgia", 10), bg="#f5f5f5")
left_language_label.grid(row=0, column=0, padx=10)

left_language_box = tk.Entry(top_frame, font=("Georgia", 10), width=25, justify="center")
left_language_box.grid(row=0, column=1)

left_audio_button = tk.Button(top_frame, text="🔊", bg="black", fg="white")
left_audio_button.grid(row=0, column=2, padx=10)

# Right language info
right_language_label = tk.Label(top_frame, text="Target Language", font=("Georgia", 10), bg="#f5f5f5")
right_language_label.grid(row=0, column=3, padx=30)

right_language_box = tk.Entry(top_frame, font=("Georgia", 10), width=25, justify="center")
right_language_box.grid(row=0, column=4)

right_audio_button = tk.Button(top_frame, text="🔊", bg="black", fg="white")
right_audio_button.grid(row=0, column=5, padx=10)

# Text areas
text_frame = tk.Frame(root, bg="#f5f5f5")
text_frame.pack(pady=20)

source_text = tk.Text(text_frame, height=15, width=40, bg="#e3e3e3", font=("Georgia", 12))
source_text.grid(row=0, column=0, padx=20)

# Swap button in the middle
swap_button = tk.Button(text_frame, text="⇄", font=("Arial", 14), bg="black", fg="white", width=4, height=2)
swap_button.grid(row=0, column=1)

target_text = tk.Text(text_frame, height=15, width=40, bg="#e3e3e3", font=("Georgia", 12))
target_text.grid(row=0, column=2, padx=20)

# Translate Button
translate_button = tk.Button(root, text="Translate", font=("Courier", 12, "bold"), bg="black", fg="white", padx=20, pady=10)
translate_button.pack(pady=10)

root.mainloop()
