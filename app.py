import streamlit as st
import requests

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

# 4. Your Unblocked GitHub Pages Live URL
pdf_url = "https://github.io"

# 5. Core PDF View Rendering & Download System
try:
    # Read the file data securely through a standard web request
    response = requests.get(pdf_url)
    pdf_bytes = response.content
    
    # Check if the file fetched successfully
    if response.status_code == 200:
        # Display the PDF on the page
        st.pdf(pdf_bytes, height=950)
        
        # Add a clean spacing layout element
        st.write("")
        
        # 6. Actionable Download Button for Anyone
        st.download_button(
            label="📥 Download Complete MS Office Training Book (PDF)",
            data=pdf_bytes,
            file_name="MS_Office_2016_Training_Guide.pdf",
            mime="application/pdf",
            type="primary"  # Makes the button stand out in bright color
        )
    else:
        st.error("Could not find the book file. Please ensure GitHub Pages is turned on in your repository settings.")
        
except Exception as e:
    st.error("Could not load the PDF file. Please verify that your public GitHub repository is live.")
