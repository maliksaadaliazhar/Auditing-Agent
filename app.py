import streamlit as st
import os
import pandas as pd
from src.receiptProcessor import process_receipt
from src.auditor import Auditor
from src.helper import draw_bounding_boxes

def main():
    st.title("AI Receipt Auditor")
    auditor = Auditor()

    uploaded_file = st.file_uploader("Upload Receipt")
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_filename = f"temp{file_ext}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        receipt = process_receipt(temp_filename)

        auditor.audit_receipt(receipt)

        # =========== Creating dataframe of results =============
        data = {
            "Merchant": [receipt.merchant_name],
            "Date": [receipt.date],
            "Total Amount (USD)": [receipt.total_amount]
        }

        df = pd.DataFrame(data)

        # ====== checking if receipt violated any rule ===========
        if receipt.flagged:
            st.error(f"Fraud Detected: {receipt.flag_reason}")
            boxes = receipt.flagged_boxes
            
            if not boxes:
                st.warning("Violation detected, but could not locate item on image.")
                st.image(temp_filename, caption="Receipt Image", use_container_width=True)
            else:
                st.info(f"Drawing {len(boxes)} red boxes...")
                annotated_image = draw_bounding_boxes(temp_filename, boxes)
                st.image(annotated_image, caption="Evidence of Violation", use_container_width=True)
        else:
            st.success("Receipt Approved")
            st.image("temp.jpg", caption="Receipt Image", use_container_width=True)

        st.write(df.head(1))

if __name__ == "__main__":
    main()
