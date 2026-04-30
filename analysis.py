import streamlit as st
from database import get_expenses
from fraud import detect_fraud

BUDGETS = {
    "Food": 300,
    "Travel": 200,
    "Office Supplies": 150
}

def show_summary():
    df = get_expenses()

    if df.empty:
        st.write("No data yet.")
        return

    df = detect_fraud(df)

    summary = df.groupby("category")["amount"].sum()
    st.bar_chart(summary)

    st.write("## 💰 Budget Tracking")

    for cat, total in summary.items():
        budget = BUDGETS.get(cat, 0)

        if total > budget:
            st.error(f"{cat}: ${total} (OVER budget ${budget})")
        else:
            st.success(f"{cat}: ${total} / ${budget}")

    st.write("## 🚨 Fraud Detection")

    fraud_cases = df[df["fraud"] == 1]

    if not fraud_cases.empty:
        st.warning("Suspicious transactions detected!")
        st.dataframe(fraud_cases)