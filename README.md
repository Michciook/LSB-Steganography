# LSB Steganography Tool

This is a university project that implements **LSB (Least Significant Bit) Steganography** to hide and extract text data within image files.

## Features

- Hide text messages inside an image.
- Extract hidden messages from an image.
- Simple **Tkinter GUI** for easy interaction.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy (`numpy`)
- Tkinter (included in Python standard library)

## How to Use

1. Run the script: `python script.py`
2. Click **Browse** to select an image file.
3. Enter text in the provided box.
4. Click **Hide data in file** to embed the text.
5. Click **Get data from file** to extract hidden text from an image.

## Notes

- The tool modifies the **least significant bits** of the image pixels to store data.
- The end of the message is marked with a special **binary sequence** (`1111111111111110`).

