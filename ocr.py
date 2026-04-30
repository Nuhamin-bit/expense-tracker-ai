from PIL import Image
import pytesseract

def extract_text(uploaded_file):
    image = Image.open(uploaded_file)
    try:
        return pytesseract.image_to_string(image)
    except Exception:
        return "OCR failed (fallback mode)"