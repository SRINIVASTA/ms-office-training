import io
import streamlit as st
from pypdf import PdfReader, PdfWriter
from streamlit_pdf_viewer import pdf_viewer
from gtts import gTTS

# 1. Universal Layout Settings
st.set_page_config(
    page_title="MS Office 2016: Complete Training Guide",
    page_icon="📚",
    layout="wide"
)

# Global CSS override to prevent clipping and style components cleanly
st.markdown("""
<style>
    [data-testid="stCustomComponentV1"] {
        overflow-x: auto !important;
        display: block;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize persistent session state for progress tracking
if "progress_tracker" not in st.session_state:
    st.session_state.progress_tracker = {}

# 2. Page Headers
st.title("📚 MS Office 2016: Complete Training Guide")
st.caption("A foundational training manual by Srinivasta — open to learners of all ages.")

# 3. Interactive Chapter Selection & Page Math
with st.sidebar:
    st.header("📖 Navigation Controls")
    
    chapter_options = {
        "1. Microsoft Word (Pages 5 - 109)": {
            "start": 5, "end": 109, "label": "MS Word", "filename": "MS_Word_Training_Guide.pdf",
            "sections": ["Word Basics & Interface", "Text Formatting & Styles", "Tables & Graphics", "Page Layout & Printing"]
        },
        "2. Microsoft Excel (Pages 110 - 259)": {
            "start": 110, "end": 259, "label": "MS Excel", "filename": "MS_Excel_Training_Guide.pdf",
            "sections": ["Excel Spreadsheet Basics", "Formulas & Basic Functions", "Data Sorting & Filtering", "Charts & Graphs"]
        },
        "3. Microsoft PowerPoint (Pages 260 - 323)": {
            "start": 260, "end": 323, "label": "MS PowerPoint", "filename": "MS_PowerPoint_Training_Guide.pdf",
            "sections": ["Presentation Basics & Layouts", "Adding Animations & Transitions", "Inserting Media & Objects", "Slide Show Delivery"]
        }
    }
    
    selected_chapter = st.selectbox(
        "Choose a Chapter to View:",
        options=list(chapter_options.keys())
    )
    
    target_start = chapter_options[selected_chapter]["start"]
    target_end = chapter_options[selected_chapter]["end"]
    chapter_name = chapter_options[selected_chapter]["label"]
    chapter_filename = chapter_options[selected_chapter]["filename"]
    chapter_sections = chapter_options[selected_chapter]["sections"]
    total_pages = target_end - target_start + 1

    page_state_key = f"current_page_{chapter_name}"
    if page_state_key not in st.session_state:
        st.session_state[page_state_key] = 1

    # Progress Tracker Checkbox UI
    st.markdown("---")
    st.subheader("✅ Chapter Milestones")
    
    completed_count = 0
    for section in chapter_sections:
        unique_key = f"{chapter_name}_{section}"
        is_checked = st.session_state.progress_tracker.get(unique_key, False)
        current_state = st.checkbox(section, value=is_checked, key=f"cb_{unique_key}")
        st.session_state.progress_tracker[unique_key] = current_state
        
        if current_state:
            completed_count += 1
            
    completion_rate = completed_count / len(chapter_sections) if chapter_sections else 0
    st.progress(completion_rate)
    st.write(f"Chapter Progress: {int(completion_rate * 100)}%")

    st.markdown("---")
    st.subheader("🔍 View Adjustments")
    zoom_level = st.slider("Adjust Viewer Width (px)", min_value=400, max_value=1400, value=850, step=50)

    st.markdown("---")
    st.subheader("⚖️ Legal Notice")
    st.warning("This material is for training purposes only and cannot be the basis for litigation.")

# 4. Process and Display the PDF securely
try:
    reader = PdfReader("MS Office Reading Material.pdf")
    
    local_current_page = st.session_state[page_state_key]
    global_pdf_page = (target_start - 1) + (local_current_page - 1)
    
    writer = PdfWriter()
    if global_pdf_page < len(reader.pages):
        writer.add_page(reader.pages[global_pdf_page])
            
    chapter_pdf_buffer = io.BytesIO()
    writer.write(chapter_pdf_buffer)
    chapter_pdf_bytes = chapter_pdf_buffer.getvalue()
    
    st.subheader(f"📖 Currently Viewing: {chapter_name}")
    st.info(f"Target Section: Page {target_start} to Page {target_end} ({total_pages} total training pages)")
    
    # Render the document viewport
    pdf_viewer(
        input=chapter_pdf_bytes,
        width=zoom_level,
        key=f"pdf_render_{chapter_name}_{local_current_page}"
    )
    
    st.markdown("---")
    
    # 5. NEW FEATURE: Dynamic Page Audio Reader Component
    st.subheader("🔊 Audio Assistant")
    active_page_object = reader.pages[global_pdf_page]
    extracted_raw_text = active_page_object.extract_text()
    
    # Clean up empty strings or generic copyright labels before vocalization processing
    clean_text = extracted_raw_text.replace("Srinivasta", "").strip() if extracted_raw_text else ""
    
    if clean_text:
        # Generate raw speech processing track in memory
        tts_engine = gTTS(text=clean_text, lang='en', slow=False)
        speech_io_buffer = io.BytesIO()
        tts_engine.write_to_fp(speech_io_buffer)
        
        # Native widget featuring multi-state Volume sliders and standard Mute actions
        st.audio(
            speech_io_buffer.getvalue(), 
            format="audio/mp3",
            start_time=0
        )
    else:
        st.caption("ℹ️ No readable text detected on this specific template layout page to speak out loud.")

    st.markdown("---")
    
    # 6. Page Scroller & Input Navigation Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("") 
        if st.button("⬅️ Previous Page", use_container_width=True):
            if st.session_state[page_state_key] > 1:
                st.session_state[page_state_key] -= 1
                st.rerun()
                
    with col2:
        jump_page = st.number_input(
            label=f"Jump to Page (1 to {total_pages})",
            min_value=1,
            max_value=total_pages,
            value=int(local_current_page),
            step=1,
            key=f"jump_input_{chapter_name}"
        )
        if jump_page != st.session_state[page_state_key]:
            st.session_state[page_state_key] = jump_page
            st.rerun()
            
        st.markdown(
            f"<p style='text-align: center; color: gray; margin: 0; font-size: 0.9rem;'>"
            f"(Manual Document Page: {target_start + local_current_page - 1})</p>", 
            unsafe_allow_html=True
        )
        
    with col3:
        st.write("") 
        if st.button("Next Page ➡️", use_container_width=True):
            if st.session_state[page_state_key] < total_pages:
                st.session_state[page_state_key] += 1
                st.rerun()

    st.markdown("---")
    
    # 7. Chapter Manual Download Action Button
    full_chapter_writer = PdfWriter()
    for p_idx in range(target_start - 1, target_end):
        if p_idx < len(reader.pages):
            full_chapter_writer.add_page(reader.pages[p_idx])
    
    full_chapter_buffer = io.BytesIO()
    full_chapter_writer.write(full_chapter_buffer)
    
    st.download_button(
        label=f"📥 Download Just Chapter: {chapter_name} (PDF)",
        data=full_chapter_buffer.getvalue(),
        file_name=chapter_filename,
        mime="application/pdf",
        type="primary"
    )
    
except FileNotFoundError:
    st.error("Missing file: Make sure 'MS Office Reading Material.pdf' is uploaded to the exact same folder as your 'app.py' on GitHub.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
