import pytesseract
from PIL import Image
import os

# Try common Windows install paths
possible_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
]

for path in possible_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

def extract_text(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)