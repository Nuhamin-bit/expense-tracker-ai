import pytesseract
from PIL import Image

def extract_text(file):
    try:
        image = Image.open(file)

        # Try OCR
        try:
            text = pytesseract.image_to_string(image)

            if not text or text.strip() == "":
                return "No text detected in receipt."

            return text

        except Exception:
            # THIS prevents Render crash
            return "OCR not available in cloud environment (Render). Using fallback mode."

    except Exception as e:
        return f"Image processing error: {str(e)}"