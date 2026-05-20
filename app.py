import base64
import io
import streamlit as st
import streamlit.components.v1 as components
from pypdf import PdfReader, PdfWriter

# 1. Universal Layout Settings
st.set_page_config(
    page_title="MS Office 2016: Complete Training Guide",
    page_icon="📚",
    layout="wide"
)

# Initialize persistent session state for tracking checkboxes
if "progress_tracker" not in st.session_state:
    st.session_state.progress_tracker = {}

# 2. Page Headers
st.title("📚 MS Office 2016: Complete Training Guide")
st.caption("A foundational training manual by Srinivasta — open to learners of all ages.")

# 3. Interactive Chapter Selection & Page Math
with st.sidebar:
    st.header("📖 Navigation Controls")
    
    # Chapter Dropdown selection mapping
    chapter_options = {
        "1. Microsoft Word (Pages 4 - 109)": {
            "start": 4, "end": 109, "label": "MS Word", "filename": "MS_Word_Training_Guide.pdf",
            "sections": ["Word Basics & Interface", "Text Formatting & Styles", "Tables & Graphics", "Page Layout & Printing"]
        },
        "2. Microsoft Excel (Pages 110 - 259)": {
            "start": 110, "end": 259, "label": "MS Excel", "filename": "MS_Excel_Training_Guide.pdf",
            "sections": ["Excel Spreadsheet Basics", "Formulas & Basic Functions", "Data Sorting & Filtering", "Charts & Graphs"]
        },
        "3. Microsoft PowerPoint (Pages 260 - 322)": {
            "start": 260, "end": 322, "label": "MS PowerPoint", "filename": "MS_PowerPoint_Training_Guide.pdf",
            "sections": ["Presentation Basics & Layouts", "Adding Animations & Transitions", "Inserting Media & Objects", "Slide Show Delivery"]
        }
    }
    
    selected_chapter = st.selectbox(
        "Choose a Chapter to View:",
        options=list(chapter_options.keys())
    )
    
    # Extract structural data based on selection
    target_start = chapter_options[selected_chapter]["start"]
    target_end = chapter_options[selected_chapter]["end"]
    chapter_name = chapter_options[selected_chapter]["label"]
    chapter_filename = chapter_options[selected_chapter]["filename"]
    chapter_sections = chapter_options[selected_chapter]["sections"]
    total_pages = target_end - target_start + 1

    # Progress Tracker Checkbox UI in Sidebar
    st.markdown("---")
    st.subheader("✅ Chapter Milestones")
    
    completed_count = 0
    for section in chapter_sections:
        # Generate a unique key for each checkbox combination
        unique_key = f"{chapter_name}_{section}"
        
        # Pull existing value or default to False
        is_checked = st.session_state.progress_tracker.get(unique_key, False)
        
        # Render the interactive checkbox
        current_state = st.checkbox(section, value=is_checked, key=f"cb_{unique_key}")
        
        # Store state updates back to session memory
        st.session_state.progress_tracker[unique_key] = current_state
        
        if current_state:
            completed_count += 1
            
    # Interactive Visual Progress Bar
    completion_rate = completed_count / len(chapter_sections)
    st.progress(completion_rate)
    st.write(f"Chapter Progress: {int(completion_rate * 100)}%")

    # Dynamic Zoom Controls
    st.markdown("---")
    st.subheader("🔍 View Adjustments")
    zoom_level = st.slider("Adjust Zoom Percentage (%)", min_value=50, max_value=200, value=100, step=10)

    st.markdown("---")
    # Page 2 Verified Legal Clause
    st.subheader("⚖️ Legal Notice")
    st.warning(
        "This material is for training purposes only and cannot be the "
        "basis for litigation. This protects you from any legal issues "
        "regarding the content of your training."
    )

# 4. Process and Display the PDF
try:
    # Read the full source PDF file
    reader = PdfReader("MS Office Reading Material.pdf")
    
    # Dynamic PDF Extraction for the active chapter
    writer = PdfWriter()
    for page_num in range(target_start - 1, target_end):
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
            
    # Save the split chapter into memory
    chapter_pdf_buffer = io.BytesIO()
    writer.write(chapter_pdf_buffer)
    chapter_pdf_bytes = chapter_pdf_buffer.getvalue()
    
    # Convert split chapter PDF to Base64 for viewing
    base64_pdf = base64.b64encode(chapter_pdf_bytes).decode('utf-8')
    
    # Context Header directly above the viewer
    st.subheader(f"📖 Currently Viewing: {chapter_name}")
    st.info(f"Target Section: Page {target_start} to Page {target_end} ({total_pages} total training pages)")
    
    # View the extracted chapter natively starting from page 1 of this sub-file
    pdf_display = (
        f'<iframe src="data:application/pdf;base64,{base64_pdf}#page=1&zoom={zoom_level}" '
        f'width="100%" height="950" type="application/pdf"></iframe>'
    )
    components.html(pdf_display, height=950)
    
    st.markdown("---")
    
    # 5. Targeted Chapter Download Button
    st.download_button(
        label=f"📥 Download Just Chapter: {chapter_name} (PDF)",
        data=chapter_pdf_bytes,
        file_name=chapter_filename,
        mime="application/pdf",
        type="primary"
    )
    
except FileNotFoundError:
    st.error("Missing file: Make sure 'MS Office Reading Material.pdf' is uploaded to the exact same folder as your 'app.py' on GitHub.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
