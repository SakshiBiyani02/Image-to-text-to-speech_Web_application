import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageEnhance, ImageTk
import pytesseract
from gtts import gTTS
import os
import subprocess
import cv2

# Set the path to the Tesseract executable
tesseract_path = r'C:\Program Files\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')

def enhance_image(img):
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    return img

def image_to_text(image_path):
    try:
        with open(image_path, 'rb') as f:
            img = Image.open(f)
            img = enhance_image(img)
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def generate_text():
    image_path = image_path_entry.get()
    if image_path:
        text = image_to_text(image_path)
        if text:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, text)

def generate_audio():
    text = result_text.get(1.0, tk.END)
    if text.strip():
        audio_path = text_to_audio(text)
        if audio_path:
            play_audio(audio_path)

def text_to_audio(text, audio_path='output_audio.mp3'):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def play_audio(audio_path):
    try:
        subprocess.Popen(['start', audio_path], shell=True)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image files", ".png;.jpg;*.jpeg")])
    if image_path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(tk.END, image_path)

def capture_image():
    try:
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        if return_value:
            cv2.imwrite("captured_image.jpg", image)
            image_path_entry.delete(0, tk.END)
            image_path_entry.insert(tk.END, "captured_image.jpg")
        camera.release()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Image OCR and Audio Generation")
root.configure(background='black')  # Set background color to black

# Create style for buttons
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", font=("Arial", 10))

# Load audio icon and resize it
audio_icon = Image.open(r"C:\Users\SAKSHI\Downloads\volume-icon-png-image_762948.png")
audio_icon = audio_icon.resize((32, 32), Image.LANCZOS)
audio_icon = ImageTk.PhotoImage(audio_icon)

# Create frame
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, padx=20, pady=20)

# Add upload image button
upload_button = ttk.Button(frame, text="Upload Image", command=open_image)
upload_button.grid(row=0, column=0, padx=10, pady=10)

# Add capture image button
capture_button = ttk.Button(frame, text="Capture Image", command=capture_image)
capture_button.grid(row=0, column=1, padx=10, pady=10)

# Add entry for image path
image_path_entry = ttk.Entry(frame, width=40)
image_path_entry.grid(row=0, column=2, padx=10, pady=10)

# Add generate text button
text_button = ttk.Button(frame, text="Generate Text", command=generate_text)
text_button.grid(row=0, column=3, padx=10, pady=10)

# Add generate audio button with resized image
audio_button = ttk.Button(frame, text="Generate Audio", image=audio_icon, compound=tk.LEFT, command=generate_audio)
audio_button.grid(row=0, column=4, padx=10, pady=10)

# Add text box to display OCR result
result_text = tk.Text(frame, height=10, width=50, wrap="word", font=("Arial", 12))
result_text.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

# Add scrollbar for text box
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=result_text.yview)
scrollbar.grid(row=1, column=5, sticky="ns")
result_text.config(yscrollcommand=scrollbar.set)

# Run the GUI
root.mainloop()
