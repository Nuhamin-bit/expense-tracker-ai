import re

def extract_amount(text):

    text = text.upper()

    # ----------------------------
    # PRIORITY 1: TOTAL KEYWORDS
    # ----------------------------
    patterns = [
        r"TOTAL\s*\$?\s*([0-9]+\.?[0-9]{0,2})",
        r"AMOUNT\s*DUE\s*\$?\s*([0-9]+\.?[0-9]{0,2})",
        r"BALANCE\s*\$?\s*([0-9]+\.?[0-9]{0,2})",
        r"PAID\s*\$?\s*([0-9]+\.?[0-9]{0,2})",
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return float(match.group(1))

    # ----------------------------
    # PRIORITY 2: ALL MONEY VALUES
    # ----------------------------
    amounts = re.findall(r"\$?\d+\.\d{2}", text)

    if amounts:
        cleaned = [float(a.replace("$", "")) for a in amounts]

        # heuristic: largest value is usually total
        return max(cleaned)

    # ----------------------------
    # FINAL FALLBACK
    # ----------------------------
    return 0.0