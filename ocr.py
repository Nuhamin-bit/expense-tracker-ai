import pytesseract
from PIL import Image

def extract_text(uploaded_file):
    image = Image.open(uploaded_file)
    return pytesseract.image_to_string(image)