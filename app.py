import streamlit as st
import requests
import base64

# 1. Universal Layout Settings
st.set_page_config(
    page_title="MS Office 2016: Complete Training Guide",
    page_icon="📚",
    layout="wide"
)

# 2. Page Headers
st.title("📚 MS Office 2016: Complete Training Guide")
st.caption("A foundational training manual by Srinivasta — open to learners of all ages.")

# 3. Structural Page Breakdown & Legal Notice
with st.sidebar:
    st.header("📖 Course Chapters")
    st.markdown("""
    - **1. Microsoft Word**
      * 105 pages of training
      * Located up to **Page 109**
    
    - **2. Microsoft Excel**
      * 150 pages of training
      * Located up to **Page 259**
    
    - **3. Microsoft PowerPoint**
      * 63 pages of training
      * Located up to **Page 322**
    """)
    st.markdown("---")
    st.info("💡 Navigation Note: Use your PDF reader's page entry box to jump straight to these target landmarks.")
    st.markdown("---")
    
    # Page 2 Verified Legal Clause
    st.subheader("⚖️ Legal Notice")
    st.warning(
        "This material is for training purposes only and cannot be the "
        "basis for litigation. This protects you from any legal issues "
        "regarding the content of your training."
    )

# 4. Your Permanent Live Release Download Link
pdf_url = "https://github.com"

# 5. Safe Base64 PDF Render Engine
try:
    # Safely download the book into memory in the backend background
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        pdf_bytes = response.content
        
        # Encode bytes to base64 string to keep it from corrupting
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Create an unblockable native HTML container string
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="950" type="application/pdf"></iframe>'
        
        # Display the PDF onto the main viewport area
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 6. Actionable Download Button for Anyone
        st.download_button(
            label="📥 Download Complete MS Office Training Book (PDF)",
            data=pdf_bytes,
            file_name="MS_Office_2016_Training_Guide.pdf",
            mime="application/pdf",
            type="primary"
        )
    else:
        st.error(f"Cannot connect to the file asset on GitHub. Server responded with status code: {response.status_code}")

except Exception as e:
    st.error(f"An error occurred while rendering the document: {e}")
