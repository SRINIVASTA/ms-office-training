import streamlit as st
import requests

# 1. Page Configuration Settings
st.set_page_config(
    page_title="MS Office 2016: Complete Training Guide",
    page_icon="📚",
    layout="wide"
)

# 2. Main Page Headers
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
    
    - **4. Microsoft PowerPoint**
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

# 4. Direct download URL from your published GitHub Release
pdf_url = "https://github.com"

# 5. Native Streamlit Rendering (Bypasses Google Iframe Bugs)
try:
    # Safely pull the bytes through Python request backend
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_bytes = response.content
        
        # Display the PDF using Streamlit's official PDF viewer engine
        st.pdf(pdf_bytes, height=950)
        
        st.markdown("---")
        # Direct Download Button
        st.download_button(
            label="📥 Download Complete MS Office Training Book (PDF)",
            data=pdf_bytes,
            file_name="MS_Office_2016_Training_Guide.pdf",
            mime="application/pdf",
            type="primary"
        )
    else:
        st.error(f"Cannot find the book.pdf asset. Status code: {response.status_code}")
except Exception as e:
    st.error(f"Error loading the book viewer: {e}")
