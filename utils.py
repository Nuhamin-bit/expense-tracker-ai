import re
from cryptography.fernet import Fernet

# Generate key (for demo)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def extract_amount(text):
    matches = re.findall(r"\$?\d+\.\d{2}", text)
    if matches:
        return float(matches[-1].replace("$", ""))
    return 0.0

def encrypt_data(text):
    return cipher.encrypt(text.encode())