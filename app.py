import streamlit as st
import pandas as pd
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

        # =========== Creating dataframe of results =============
        data = {
            "Merchant": [receipt.merchant_name],
            "Date": [receipt.date],
            "Total Amount (USD)": [receipt.total_amount]
        }

        df = pd.DataFrame(data)
        st.write(df.head(1))

        # ====== checking if receipt violated any rule ===========
        if receipt.flagged:
            st.error(f"Fraud Detected : {receipt.flag_reason}")
        else:
            st.success("Receipt Approved")

if __name__ == "__main__":
    main()
