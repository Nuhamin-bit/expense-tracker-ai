import streamlit as st
import pandas as pd

from ocr import extract_text
from analysis import show_summary
from classifier import predict_category
from database import add_expense, get_expenses

# Optional fraud detection (safe import)
try:
    from fraud import apply_fraud_detection
    FRAUD_AVAILABLE = True
except:
    FRAUD_AVAILABLE = False


# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="AI Expense Tracker", layout="wide")

st.title("📊 AI-Powered Expense & Budget Tracker")
st.write("Upload receipts to automatically extract, categorize, and analyze spending.")

st.info("⚠️ OCR works locally. Cloud deployment uses fallback processing for stability.")


# ----------------------------
# UPLOAD RECEIPT
# ----------------------------
uploaded_file = st.file_uploader("📤 Upload Receipt Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:

    # ----------------------------
    # OCR PROCESSING (SAFE)
    # ----------------------------
    text = extract_text(uploaded_file)

    st.subheader("🧾 Extracted Text")
    st.text_area("Receipt Text", text, height=200)

    # ----------------------------
    # AMOUNT EXTRACTION (SAFE)
    # ----------------------------
    import re

    amounts = re.findall(r"\$?\d+\.\d{2}", text)
    amount = float(amounts[-1].replace("$", "")) if amounts else 0.0

    st.subheader("💰 Detected Amount")
    st.write(f"${amount}")

    # ----------------------------
    # CATEGORY PREDICTION (ML)
    # ----------------------------
    category = predict_category(text)

    st.subheader("🤖 Category (AI Model)")
    st.write(category)

    # ----------------------------
    # SAVE TO DATABASE
    # ----------------------------
    add_expense(amount, category, text)

    st.success("Receipt processed and saved successfully!")

# ----------------------------
# DASHBOARD
# ----------------------------
st.markdown("---")
st.subheader("📈 Expense Dashboard")

df = get_expenses()

if len(df) > 0:

    # Convert amount column safely
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # ----------------------------
    # FRAUD DETECTION (OPTIONAL)
    # ----------------------------
    if FRAUD_AVAILABLE:
        df = apply_fraud_detection(df)

    # ----------------------------
    # METRICS
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Spending", f"${df['amount'].sum():.2f}")
    col2.metric("📊 Avg Expense", f"${df['amount'].mean():.2f}")
    col3.metric("🧾 Transactions", len(df))

    # ----------------------------
    # CHART
    # ----------------------------
    st.subheader("📊 Spending by Category")
    chart_data = df.groupby("category")["amount"].sum()
    st.bar_chart(chart_data)

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("📜 Recent Transactions")

    if FRAUD_AVAILABLE:
        st.dataframe(df[["amount", "category", "fraud_flag"]].tail(10))
    else:
        st.dataframe(df.tail(10))

else:
    st.warning("No expenses found yet. Upload a receipt to begin.")