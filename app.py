import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LSB-STEGANOGRAPHY")
        self.geometry("400x300")

        self.label = tk.Label(self, text="Choose a file", wraplength=380)
        self.label.pack(pady=10)

        self.button_browse = tk.Button(self, text="Browse", command=self.browse_file)
        self.button_browse.pack(pady=5)

        self.text_box = tk.Text(self, height=5, width=30)
        self.text_box.pack(pady=10)

        self.button_process = tk.Button(self, text="Hide data in file", command=self.hide_in_file, state=tk.DISABLED)
        self.button_process.pack(pady=5)

        self.button_extract = tk.Button(self, text="Get data from file", command=self.get_from_file, state=tk.DISABLED)
        self.button_extract.pack(pady=5)

        self.selected_file = None


    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Choose a file")
        if file_path:
            self.selected_file = file_path
            self.label.config(text=f"{file_path}")
            self.button_process.config(state=tk.NORMAL)
            self.button_extract.config(state=tk.NORMAL)


    def hide_in_file(self):
        if self.selected_file:
            self.label.config(text=f"Processing: {self.selected_file}")
            self.hide_text(self.selected_file, self.text_box.get("1.0", tk.END).strip(), f"output.{self.selected_file.split(".")[-1]}")


    def get_from_file(self):
        if self.selected_file:
            self.label.config(text=f"Processing: {self.selected_file}")
            self.extract_text(self.selected_file)


    def text_to_bin(self, text):
        return ''.join(format(ord(i), '08b') for i in text)


    def bin_to_text(self, binary_data):
        text = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
        return text


    def hide_text(self, image_path, text, output_path):
        try:
            image = cv2.imread(image_path)
            if image is None:
                messagebox.showerror("Error", "Could not open the image file.")
                return
            bin_text = self.text_to_bin(text) + '1111111111111110'

            bin_text = bin_text.ljust((len(bin_text) + 2) // 3 * 3, '0')
            message_bits = np.array([int(bin_text[i:i+3], 2) for i in range(0, len(bin_text), 3)], dtype=np.uint8)

            flat_image = image.flatten()
            if len(message_bits) > len(flat_image):
                messagebox.showerror("Error", "Message too large to hide in this image.")
                return
        
            flat_image[:len(message_bits)] = (flat_image[:len(message_bits)] & 0xF8) | message_bits

            encoded_image = flat_image.reshape(image.shape)
            cv2.imwrite(output_path, encoded_image)
            self.label.config(text=f"Data saved!")
        except Exception as e:
             messagebox.showerror("Error", f"An error occurred: {e}")

    
    def extract_text(self, image_path):
        try:
            image = cv2.imread(image_path)
            if image is None:
                messagebox.showerror("Error", "Could not open the image file.")
                return

            binary_data = np.bitwise_and(image.flatten(), 0x07)
            binary_data = ''.join(format(byte, '03b') for byte in binary_data)

            end_marker = "1111111111111110"
            end_idx = binary_data.find(end_marker)
            if end_idx != -1:
                binary_data = binary_data[:end_idx]

            messagebox.showinfo("Success", f"Data was extracted! \nData: {self.bin_to_text(binary_data)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
