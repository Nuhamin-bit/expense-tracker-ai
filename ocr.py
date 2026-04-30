import pytesseract
from PIL import Image

def extract_text(file):
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)

        # If OCR fails or returns empty
        if not text or text.strip() == "":
            return "No text detected in receipt."

        return text

    except Exception as e:
        # IMPORTANT: prevents Render crash
        return f"OCR unavailable in cloud environment. Error: {str(e)}"