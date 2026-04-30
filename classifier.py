def predict_category(text):

    text = text.lower()

    if "fuel" in text or "gas" in text:
        return "Travel", 85
    elif "restaurant" in text or "food" in text:
        return "Food", 80
    elif "uber" in text:
        return "Transport", 78
    else:
        return "Other", 60