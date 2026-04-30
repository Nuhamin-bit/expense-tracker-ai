import streamlit as st
from PIL import Image
from datetime import datetime

from ocr import extract_text
from classifier import predict_category
from database import insert_expense, get_expenses
from analysis import show_summary
from utils import extract_amount, encrypt_data

# -----------------------
# STREAMLIT CONFIG
# -----------------------
st.set_page_config(page_title="AI Expense Tracker", layout="wide")

st.title("📊 AI-Powered Expense & Budget Tracker")
st.write("Upload receipts to automatically extract, categorize, and analyze spending.")

# -----------------------
# UPLOAD RECEIPT
# -----------------------
uploaded_file = st.file_uploader("📤 Upload Receipt Image", type=["jpg", "png", "jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)

    if st.button("🚀 Process Receipt"):

        # OCR
        text = extract_text(uploaded_file)

        # AI classification (ML model)
        category = predict_category(text)

        # Extract amount
        amount = extract_amount(text)

        # Encrypt raw receipt text (security requirement)
        encrypted_text = encrypt_data(text)

        # Store in database
        insert_expense(
            encrypted_text,
            category,
            amount,
            datetime.now().strftime("%Y-%m-%d")
        )

        # -----------------------
        # RESULTS DISPLAY
        # -----------------------
        st.success("✅ Receipt Processed Successfully!")

        st.write("### 🧾 Extracted Text")
        st.text(text)

        st.write("### 💰 Detected Amount")
        st.metric("Amount", f"${amount}")

        st.write("### 🤖 Category (AI Model)")
        st.success(category)

# -----------------------
# DASHBOARD SECTION
# -----------------------
st.write("---")
st.header("📊 Analytics Dashboard")

show_summary()

# -----------------------
# DATABASE VIEW
# -----------------------
st.write("---")
st.header("📂 Stored Expenses")

df = get_expenses()
st.dataframe(df)