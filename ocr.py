from PIL import Image

def extract_text(file):
    """
    Cloud-safe OCR fallback system.
    Never crashes on Render.
    """

    try:
        image = Image.open(file)

        # Try OCR only if available
        try:
            import pytesseract
            text = pytesseract.image_to_string(image)

            if text and text.strip():
                return text

            return "No text detected in receipt."

        except Exception:
            # 🚨 CRITICAL FIX: prevents Render crash
            return (
                "OCR not available in cloud environment.\n"
                "Receipt uploaded successfully (fallback mode active)."
            )

    except Exception as e:
        return f"Image processing error: {str(e)}"