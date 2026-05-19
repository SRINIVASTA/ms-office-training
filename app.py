import streamlit as st

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

# 4. Your Permanent Live Release Link
# This pulls directly from the v1.0.0 release asset you just published
pdf_url = "https://github.com"

# 5. Safe Embedded Document Viewer Layout
google_view_url = f"https://google.com{pdf_url}&embedded=true"
st.components.v1.iframe(google_view_url, height=950, scrolling=True)

# 6. Actionable Download Button for Anyone
st.markdown("---")
st.markdown(f'<a href="{pdf_url}" target="_blank"><button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; border-radius:4px; font-weight:bold; cursor:pointer;">📥 Click Here to Download Full PDF Book (25MB)</button></a>', unsafe_allow_html=True)
