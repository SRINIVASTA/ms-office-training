import io
import streamlit as st
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_bytes

# 1. Universal Layout Settings
st.set_page_config(
    page_title="MS Office 2016: Complete Training Guide",
    page_icon="📚",
    layout="wide"
)

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
    zoom_level = st.slider("Adjust Document Size (px width)", min_value=400, max_value=1400, value=850, step=50)

# 4. Process and Display the PDF Securely via Image Extraction
try:
    reader = PdfReader("MS Office Reading Material.pdf")
    local_current_page = st.session_state[page_state_key]
    global_pdf_page = (target_start - 1) + (local_current_page - 1)
    
    # Isolate single page binary
    writer = PdfWriter()
    if global_pdf_page < len(reader.pages):
        writer.add_page(reader.pages[global_pdf_page])
            
    chapter_pdf_buffer = io.BytesIO()
    writer.write(chapter_pdf_buffer)
    chapter_pdf_bytes = chapter_pdf_buffer.getvalue()
    
    st.subheader(f"📖 Currently Viewing: {chapter_name}")
    st.info(f"Target Section: Page {target_start} to Page {target_end} ({total_pages} total training pages)")
    
    # UNBLOCKED RENDER LAYER: Converts document bytes to image frames to prevent iframe block bugs
    rendered_pages_list = convert_from_bytes(chapter_pdf_bytes, dpi=130)
    if rendered_pages_list:
        col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
        with col_img2:
            st.image(rendered_pages_list[0], width=zoom_level)
    else:
        st.error("Could not render page canvas.")

    st.markdown("---")
    
    # 5. Native Streamlit Layout Pagination Bar
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
    
    # 6. KINDLE SHADOW TEXT SYNCHRONIZED READER PANEL (READ-ALOUD LAYER)
    st.subheader("🔊 Amazon Kindle-Style Interactive Audiobook Player")
    
    active_page_object = reader.pages[global_pdf_page]
    extracted_raw_text = active_page_object.extract_text()
    clean_text = extracted_raw_text.replace("Srinivasta", "").strip() if extracted_raw_text else ""
    js_safe_text = clean_text.replace('"', '\\"').replace('\n', ' ') if clean_text else "No text found on page."
    
    html_amazon_reader = f"""
    <div style="font-family: 'Segoe UI', system-ui, sans-serif; background-color: #fcfbf7; padding: 25px; border-radius: 8px; border: 1px solid #e6e3da;">
        
        <div style="margin-bottom: 20px; display: flex; gap: 10px; align-items: center;">
            <button id="btn-play" onclick="startAmazonSpeech()" style="padding: 10px 22px; background-color: #fad160; color: #111; border: 1px solid #e6b422; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 0.95rem;">▶ Read Out Loud</button>
            <button id="btn-stop" onclick="stopAmazonSpeech()" style="padding: 10px 22px; background-color: #f0f2f6; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-weight: 500; font-size: 0.95rem;">⏸ Pause</button>
            <span id="tracker-status" style="margin-left: auto; font-size: 0.85rem; color: #777; font-weight: 500;">Status: Ready to track</span>
        </div>
        
        <div id="kindle-text-deck" style="font-size: 1.25rem; line-height: 2.1rem; color: #222; text-align: justify; font-family: Georgia, serif; max-height: 250px; overflow-y: auto; background: white; padding: 15px; border: 1px solid #eee; border-radius: 4px;"></div>
    </div>

    <script>
        const rawContent = "{js_safe_text}";
        const textContainer = document.getElementById("kindle-text-deck");
        const statusLabel = document.getElementById("tracker-status");
        
        const textWordsArray = rawContent.split(" ");
        textContainer.innerHTML = textWordsArray.map((word, idx) => `<span id="t-word-${{idx}}" style="padding: 1px 2px; margin: 0 1px; border-radius: 3px;">${{word}}</span>`).join(" ");
        
        let voiceSynth = window.speechSynthesis;
        let utterInstance = null;
        
        function startAmazonSpeech() {{
            voiceSynth.cancel();
            statusLabel.innerText = "Status: Highlighting Line Tracking...";
            statusLabel.style.color = "#2eb85c";
            
            utterInstance = new SpeechSynthesisUtterance(rawContent);
            utterInstance.lang = 'en-US';
            utterInstance.rate = 0.95;
            
            utterInstance.onboundary = function(event) {{
                if (event.name === 'word') {{
                    const characterIndex = event.charIndex;
                    const textChunk = rawContent.substring(0, characterIndex).trim();
                    const currentWordPointer = textChunk ? textChunk.split(" ").length : 0;
                    
                    document.querySelectorAll("#kindle-text-deck span").forEach(node => {{
                        node.style.backgroundColor = "transparent";
                        node.style.boxShadow = "none";
                    }});
                    
                    const activeNode = document.getElementById(`t-word-${{currentWordPointer}}`);
                    if (activeNode) {{
                        activeNode.style.backgroundColor = "#fff2a3";
                        activeNode.style.boxShadow = "0 1px 5px #fff2a3";
                        activeNode.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                    }}
                }}
            }};
            
            utterInstance.onend = function() {{
                statusLabel.innerText = "Status: Page Reading Completed";
                statusLabel.style.color = "#777";
                document.querySelectorAll("#kindle-text-deck span").forEach(node => {{
                    node.style.backgroundColor = "transparent";
                }});
            }};
            
            voiceSynth.speak(utterInstance);
        }}
        
        function stopAmazonSpeech() {{
            voiceSynth.cancel();
            statusLabel.innerText = "Status: Paused";
            statusLabel.style.color = "#dc3545";
        }}
    </script>
    """
    st.components.v1.html(html_amazon_reader, height=350, scrolling=False)

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
