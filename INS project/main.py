import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# Convert data to binary format
def to_bin(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])
    elif isinstance(data, int):
        return format(data, '08b')
    elif isinstance(data, bytes):
        return [format(i, '08b') for i in data]
    else:
        raise TypeError("Input type not supported")

# Encode the message into the image
def encode_image(image_path, secret_message, output_image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = list(image.getdata())
    binary_message = to_bin(secret_message) + to_bin('###')  # Marking the end with ###
    message_len = len(binary_message)
    
    new_pixels = []
    pixel_idx = 0
    for pixel in pixels:
        if pixel_idx < message_len:
            r, g, b = pixel
            r = int(to_bin(r)[:-1] + binary_message[pixel_idx], 2)
            pixel_idx += 1
        else:
            r, g, b = pixel
        new_pixels.append((r, g, b))

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_image_path)
    messagebox.showinfo("Success", f"Message encoded successfully into {output_image_path}")

# Decode the hidden message from the image
def decode_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = list(image.getdata())

    binary_message = ""
    for pixel in pixels:
        r, g, b = pixel
        binary_message += to_bin(r)[-1]
    
    binary_message_split = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ""
    for byte in binary_message_split:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-3:] == "###":
            break
    return decoded_message[:-3]

# GUI Implementation using Tkinter
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("500x300")

        # Labels and Entry fields
        self.label = tk.Label(root, text="Enter Secret Message:")
        self.label.pack(pady=10)
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=10)

        # Buttons
        self.encode_button = tk.Button(root, text="Encode Message", command=self.encode)
        self.encode_button.pack(pady=5)

        self.decode_button = tk.Button(root, text="Decode Message", command=self.decode)
        self.decode_button.pack(pady=5)

        # Image path for later use
        self.image_path = None

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if self.image_path:
            messagebox.showinfo("Image Selected", f"Image: {os.path.basename(self.image_path)} loaded successfully.")

    def encode(self):
        self.open_image()
        if not self.image_path:
            return
        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Input Error", "Please enter a message to encode!")
            return
        
        output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if not output_image_path:
            return
        
        # Encode the message
        encode_image(self.image_path, message, output_image_path)

    def decode(self):
        self.open_image()
        if not self.image_path:
            return
        
        # Decode the message
        hidden_message = decode_image(self.image_path)
        messagebox.showinfo("Decoded Message", f"Hidden Message: {hidden_message}")

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
