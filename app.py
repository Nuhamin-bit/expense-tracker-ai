import streamlit as st
import re

from database import (
    init_db,
    add_expense,
    get_expenses,
    set_budget,
    get_budgets
)

from ocr import extract_text

# ---------------- INIT ----------------
init_db()

st.set_page_config(page_title="AI Expense Tracker", layout="centered")

st.title("📊 AI Expense & Budget Tracker")
st.write("Upload receipts, track spending, and manage budgets")

# ---------------- UPLOAD RECEIPT ----------------
uploaded_file = st.file_uploader("📤 Upload Receipt Image")

if uploaded_file:

    # OCR
    text = extract_text(uploaded_file)

    st.subheader("🧾 Extracted Receipt Text")
    st.text_area("", text, height=200)

    # ---------------- AMOUNT EXTRACTION ----------------
    amounts = re.findall(r"\d+\.\d{2}", text)
    amount = float(amounts[0]) if amounts else 0.0

    # ---------------- CATEGORY LOGIC ----------------
    text_lower = text.lower()

    if "fuel" in text_lower or "gas" in text_lower:
        category = "Travel"
    elif "grocery" in text_lower or "food" in text_lower:
        category = "Food"
    else:
        category = "Other"

    # ---------------- SAVE ----------------
    add_expense(amount, category, text)

    st.success("Transaction saved successfully!")

    st.subheader("💵 Detected Amount")
    st.write(f"${amount:.2f}")

    st.subheader("📂 Category")
    st.write(category)

# ---------------- DASHBOARD ----------------
st.divider()
st.subheader("📈 Spending Dashboard")

expenses = get_expenses()

total_spent = sum([e[0] for e in expenses])
transaction_count = len(expenses)

st.metric("Total Spending", f"${total_spent:.2f}")
st.metric("Transactions", transaction_count)

# category breakdown
category_totals = {}
for amount, cat in expenses:
    category_totals[cat] = category_totals.get(cat, 0) + amount

st.bar_chart(category_totals)

# ---------------- BUDGET SETTING ----------------
st.divider()
st.subheader("💰 Set Monthly Budget")

with st.form("budget_form"):
    category = st.selectbox("Category", ["Food", "Travel", "Other"])
    limit = st.number_input("Monthly Budget ($)", min_value=0.0, step=10.0)

    submit = st.form_submit_button("Set Budget")

    if submit:
        set_budget(category, limit)
        st.success(f"Budget set: {category} = ${limit:.2f}")

# ---------------- BUDGET ALERTS ----------------
st.subheader("⚠️ Budget Status")

budgets = get_budgets()

if budgets:
    for cat, spent in category_totals.items():
        if cat in budgets:
            limit = budgets[cat]

            if spent > limit:
                st.error(f"🚨 {cat}: OVER BUDGET (${spent:.2f} / ${limit:.2f})")
            else:
                st.success(f"✅ {cat}: OK (${spent:.2f} / ${limit:.2f})")
else:
    st.info("No budgets set yet.")