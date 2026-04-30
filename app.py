import streamlit as st
import pandas as pd
import re
import numpy as np

from classifier import predict_category
from database import add_expense, get_expenses


# ----------------------------
# SAFE OCR WRAPPER (NO CRASH)
# ----------------------------
def safe_extract_text(file):
    try:
        from ocr import extract_text
        return extract_text(file)
    except:
        return f"Receipt uploaded: {file.name}"


# ----------------------------
# RECEIPT PARSER (ENHANCED)
# ----------------------------
def parse_receipt(text):
    text = text.upper()

    def find(patterns):
        for p in patterns:
            m = re.search(p, text)
            if m:
                return float(m.group(1))
        return None

    total = find([
        r"TOTAL\s*\$?\s*([0-9]+\.?[0-9]{2})",
        r"AMOUNT\s*DUE\s*\$?\s*([0-9]+\.?[0-9]{2})",
        r"BALANCE\s*\$?\s*([0-9]+\.?[0-9]{2})",
    ])

    subtotal = find([r"SUBTOTAL\s*\$?\s*([0-9]+\.?[0-9]{2})"])
    tax = find([r"TAX\s*\$?\s*([0-9]+\.?[0-9]{2})"])
    gallons = find([r"GALLONS\s*([0-9]+\.?[0-9]*)"])

    return {
        "total": total or 0.0,
        "subtotal": subtotal or 0.0,
        "tax": tax or 0.0,
        "gallons": gallons or 0.0
    }


# ----------------------------
# FRAUD DETECTION (ANOMALY LOGIC)
# ----------------------------
def fraud_score(amount, df):
    if len(df) < 5:
        return 0  # not enough data

    mean = df["amount"].mean()
    std = df["amount"].std() if df["amount"].std() > 0 else 1

    z_score = abs((amount - mean) / std)

    if z_score > 3:
        return 90  # high risk
    elif z_score > 2:
        return 60  # medium risk
    elif z_score > 1.5:
        return 30  # low risk
    else:
        return 5   # normal


# ----------------------------
# CONFIDENCE SCORE (AI QUALITY METRIC)
# ----------------------------
def confidence_score(text, parsed):
    score = 50

    if parsed["total"] > 0:
        score += 20
    if parsed["tax"] > 0:
        score += 10
    if parsed["subtotal"] > 0:
        score += 10
    if "TOTAL" in text.upper():
        score += 10

    return min(score, 100)


# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="AI Expense Tracker", layout="wide")

st.title("📊 AI Expense & Budget Intelligence System")
st.caption("Smart Receipt Processing • Fraud Detection • Budget Analytics")

uploaded_file = st.file_uploader("📤 Upload Receipt Image", type=["jpg", "png", "jpeg"])

df = get_expenses()
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)


# ----------------------------
# MAIN PROCESSING
# ----------------------------
if uploaded_file:

    text = safe_extract_text(uploaded_file)
    parsed = parse_receipt(text)

    amount = parsed["total"]

    category = predict_category(text)

    fraud = fraud_score(amount, df)
    confidence = confidence_score(text, parsed)

    # ----------------------------
    # DISPLAY RECEIPT
    # ----------------------------
    st.subheader("🧾 Receipt Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total", f"${amount:.2f}")
    col2.metric("🤖 Category", category)
    col3.metric("🧠 Confidence", f"{confidence}%")

    st.progress(confidence / 100)

    # ----------------------------
    # FRAUD ALERT
    # ----------------------------
    if fraud > 70:
        st.error("🚨 HIGH FRAUD RISK DETECTED")
    elif fraud > 40:
        st.warning("⚠️ Medium risk transaction")
    else:
        st.success("✅ Normal transaction")

    st.caption(f"Fraud Score: {fraud}/100")

    # ----------------------------
    # BREAKDOWN
    # ----------------------------
    st.subheader("📊 Financial Breakdown")

    c1, c2, c3 = st.columns(3)
    c1.metric("Subtotal", f"${parsed['subtotal']:.2f}")
    c2.metric("Tax", f"${parsed['tax']:.2f}")
    c3.metric("Gallons", parsed["gallons"])

    # ----------------------------
    # SAVE
    # ----------------------------
    add_expense(amount, category, text)

    st.success("Transaction saved successfully!")


# ----------------------------
# DASHBOARD
# ----------------------------
st.markdown("---")
st.subheader("📈 Business Dashboard")

if len(df) > 0:

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Spending", f"${df['amount'].sum():.2f}")
    c2.metric("Average Expense", f"${df['amount'].mean():.2f}")
    c3.metric("Transactions", len(df))

    st.subheader("📊 Category Breakdown")
    st.bar_chart(df.groupby("category")["amount"].sum())

    st.subheader("📜 Recent Transactions")
    st.dataframe(df.tail(10))

else:
    st.info("Upload receipts to build your financial dashboard.")