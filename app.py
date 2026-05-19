import streamlit as st

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

# 4. Your Unblocked GitHub Pages Live Link
pdf_url = "https://github.io"

# 5. Safe Multi-Page Heavy Iframe Embed (Bypasses the 25MB local crash limit)
google_view_url = f"https://google.com{pdf_url}&embedded=true"

# Embed the large book viewer cleanly
st.components.v1.iframe(google_view_url, height=900, scrolling=True)

# 6. Instant Direct File Download
st.markdown("---")
st.markdown(f'<a href="{pdf_url}" target="_blank"><button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; border-radius:4px; font-weight:bold; cursor:pointer;">📥 Click Here to Download Full PDF Book (25MB)</button></a>', unsafe_allow_html=True)
