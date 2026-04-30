from PIL import Image

def extract_text(file):
    """
    Safe OCR wrapper:
    - Never crashes on Render
    - Falls back gracefully if OCR is unavailable
    """

    try:
        image = Image.open(file)

        # Try importing pytesseract ONLY when needed
        try:
            import pytesseract
            text = pytesseract.image_to_string(image)

            if not text or text.strip() == "":
                return "No text detected in receipt."

            return text

        except Exception:
            # THIS prevents Render crash permanently
            return "OCR unavailable on cloud deployment (Render). Receipt processed in fallback mode."

    except Exception as e:
        return f"Image loading error: {str(e)}"