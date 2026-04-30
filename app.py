import streamlit as st
from PIL import Image

from ocr import extract_text
from receipt_parser import parse_receipt
from classifier import predict_category
from database import init_db, add_expense, get_expenses
from fraud_model import train_fraud_model, detect_fraud
from budget import set_budget, get_budgets, check_budget_status

import pandas as pd


# ----------------------------
# INIT
# ----------------------------
init_db()
st.set_page_config(page_title="AI Expense System", layout="wide")

st.title("📊 AI Expense & Budget Intelligence System")


# ----------------------------
# SIDEBAR - BUDGET
# ----------------------------
st.sidebar.header("💰 Budget Setup")

cat_input = st.sidebar.text_input("Category")
limit_input = st.sidebar.number_input("Monthly Limit", min_value=0.0)

if st.sidebar.button("Set Budget"):
    if cat_input:
        set_budget(cat_input, limit_input)
        st.sidebar.success("Budget saved!")


# ----------------------------
# UPLOAD RECEIPT
# ----------------------------
uploaded_file = st.file_uploader("Upload Receipt", type=["png", "jpg", "jpeg"])


if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Receipt")

    # OCR
    text = extract_text(uploaded_file)

    st.subheader("🧾 Extracted Text")
    st.write(text)

    # Parsing
    parsed = parse_receipt(text)

    amount = parsed["total"]
    subtotal = parsed["subtotal"]
    tax = parsed["tax"]
    gallons = parsed["gallons"]

    # ML Category
    category, confidence = predict_category(text)

    # ----------------------------
    # FRAUD MODEL
    # ----------------------------
    df = get_expenses()
    model = train_fraud_model(df)

    fraud_score = detect_fraud(model, amount)

    # ----------------------------
    # SAVE TO DB
    # ----------------------------
    add_expense(amount, category, text)

    st.success("Transaction saved!")


    # ----------------------------
    # DISPLAY RESULTS
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total", f"${amount:.2f}")
    col2.metric("🤖 Category", category)
    col3.metric("🧠 Confidence", f"{confidence}%")


    st.subheader("🚨 Fraud Detection")

    if fraud_score > 70:
        st.error(f"High Fraud Risk: {fraud_score}/100")
    elif fraud_score > 30:
        st.warning(f"Medium Risk: {fraud_score}/100")
    else:
        st.success(f"Normal Transaction: {fraud_score}/100")


    st.subheader("📊 Breakdown")
    st.write(f"Subtotal: ${subtotal}")
    st.write(f"Tax: ${tax}")
    st.write(f"Gallons: {gallons}")


# ----------------------------
# DASHBOARD
# ----------------------------
st.markdown("---")
st.subheader("📈 Dashboard")

df = get_expenses()

if not df.empty:

    total = df["amount"].sum()
    avg = df["amount"].mean()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Spending", f"${total:.2f}")
    c2.metric("Average", f"${avg:.2f}")
    c3.metric("Transactions", len(df))

    st.subheader("📊 Category Breakdown")
    st.bar_chart(df["category"].value_counts())

    # ----------------------------
    # BUDGET CHECK
    # ----------------------------
    st.subheader("💰 Budget Status")

    budgets = dict(get_budgets())

    for cat, limit in budgets.items():
        spent = df[df["category"] == cat]["amount"].sum()
        status = check_budget_status(cat, spent)

        st.write(f"**{cat}**: ${spent:.2f} / ${limit}")

        if status == "❌ OVER BUDGET":
            st.error(status)
        elif status == "⚠️ WARNING":
            st.warning(status)
        else:
            st.success(status)

else:
    st.info("No transactions yet.")