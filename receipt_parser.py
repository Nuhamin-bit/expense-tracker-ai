import re

def parse_receipt(text):
    text = text.upper()

    def find(patterns):
        for p in patterns:
            m = re.search(p, text)
            if m:
                try:
                    return float(m.group(1))
                except:
                    pass
        return 0.0

    return {
        "total": find([r"TOTAL\s*\$?(\d+\.?\d*)"]),
        "subtotal": find([r"SUBTOTAL\s*\$?(\d+\.?\d*)"]),
        "tax": find([r"TAX\s*\$?(\d+\.?\d*)"]),
        "gallons": find([r"GALLONS\s*(\d+\.?\d*)"])
    }