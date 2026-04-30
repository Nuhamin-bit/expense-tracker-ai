import streamlit as st
from PIL import Image

# Local modules
from ocr import extract_text
from receipt_parser import parse_receipt
from classifier import predict_category
from database import add_expense, get_expenses


# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Expense & Budget Intelligence System")
st.subheader("Smart Receipt Processing • Categorization • Analytics")


# ----------------------------
# SIDEBAR - UPLOAD
# ----------------------------
st.sidebar.header("📤 Upload Receipt")

uploaded_file = st.sidebar.file_uploader(
    "Upload receipt image",
    type=["png", "jpg", "jpeg"]
)


# ----------------------------
# MAIN LOGIC
# ----------------------------
if uploaded_file:

    # Show image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    # OCR STEP
    text = extract_text(uploaded_file)

    st.markdown("## 🧾 Extracted Text")
    st.write(text)

    # ----------------------------
    # PARSE RECEIPT (SAFE)
    # ----------------------------
    parsed = parse_receipt(text)

    amount = parsed.get("total", 0.0)
    subtotal = parsed.get("subtotal", 0.0)
    tax = parsed.get("tax", 0.0)
    gallons = parsed.get("gallons", 0.0)

    # ----------------------------
    # ML CATEGORY
    # ----------------------------
    category, confidence = predict_category(text)

    # ----------------------------
    # FRAUD DETECTION (RULE-BASED MVP)
    # ----------------------------
    fraud_score = 0

    if amount > 500:
        fraud_score += 40
    if "REFUND" in text.upper():
        fraud_score += 30
    if amount == 0:
        fraud_score += 50

    fraud_label = "⚠️ Suspicious" if fraud_score > 50 else "✅ Normal"


    # ----------------------------
    # UI RESULTS
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💵 Total", f"${amount:.2f}")

    with col2:
        st.metric("🤖 Category", category)

    with col3:
        st.metric("🧠 Confidence", f"{confidence}%")

    st.markdown("### 🚨 Fraud Analysis")
    st.write(f"Fraud Score: **{fraud_score}/100**")
    st.write(f"Status: {fraud_label}")

    # ----------------------------
    # BREAKDOWN
    # ----------------------------
    st.markdown("### 📊 Financial Breakdown")

    b1, b2, b3 = st.columns(3)

    b1.metric("Subtotal", f"${subtotal:.2f}")
    b2.metric("Tax", f"${tax:.2f}")
    b3.metric("Gallons", f"{gallons:.2f}")


    # ----------------------------
    # SAVE TO DATABASE
    # ----------------------------
    add_expense(amount, category, text)

    st.success("Transaction saved successfully!")


# ----------------------------
# DASHBOARD (HISTORY)
# ----------------------------
st.markdown("---")
st.markdown("## 📈 Business Dashboard")

df = get_expenses()

if not df.empty:

    total_spending = df["amount"].sum()
    avg_expense = df["amount"].mean()
    count = len(df)

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Spending", f"${total_spending:.2f}")
    c2.metric("Average Expense", f"${avg_expense:.2f}")
    c3.metric("Transactions", count)

    st.markdown("### 📊 Category Breakdown")
    st.bar_chart(df["category"].value_counts())

else:
    st.info("No transactions yet. Upload a receipt to begin.")