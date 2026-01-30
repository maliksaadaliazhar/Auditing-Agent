import streamlit as st
from src.receiptProcessor import process_receipt
from src.auditor import Auditor

def main():
    st.title("AI Receipt Auditor")
    auditor = Auditor()

    uploaded_file = st.file_uploader("Upload Receipt")
    if uploaded_file:
        with open("temp.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        receipt = process_receipt("temp.jpg")

        auditor.audit_receipt(receipt)
        st.write(f"Merchant: {receipt.merchant_name}")
        if receipt.flagged:
            st.error(f"Fraud Detected : {receipt.flag_reason}")
        else:
            st.success("Receipt Approved")

if __name__ == "__main__":
    main()
