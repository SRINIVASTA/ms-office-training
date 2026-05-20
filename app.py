import io
import streamlit as st
from pypdf import PdfReader, PdfWriter

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
    zoom_level = st.slider("Adjust Text Reading Panel Width (px)", min_value=500, max_value=1400, value=950, step=50)

# 4. Process and Display the PDF with Real-Time Amazon Kinetic Highlights
try:
    # Safely load document pages from local environment storage file
    with open("MS Office Reading Material.pdf", "rb") as raw_file:
        raw_pdf_bytes = raw_file.read()
        
    reader = PdfReader(io.BytesIO(raw_pdf_bytes))
    local_current_page = st.session_state[page_state_key]
    global_pdf_page = (target_start - 1) + (local_current_page - 1)
    
    # Target and capture original text formatting from the manual layout layer
    active_page_object = reader.pages[global_pdf_page]
    extracted_raw_text = active_page_object.extract_text()
    
    # Filter away common repeating background names or footers safely
    clean_text = extracted_raw_text.replace("Srinivasta", "").strip() if extracted_raw_text else ""
    js_safe_text = clean_text.replace('"', '\\"').replace('\n', ' ') if clean_text else "No text found on page."
    
    st.subheader(f"📖 Kindle-Style Reading Dashboard: {chapter_name}")
    st.info(f"Target Section: Page {target_start} to Page {target_end} ({total_pages} total training pages)")
    
    # 5. AMAZON KINDLE-STYLE FLOATING SHADOW CANVAS COMPONENT
    amazon_reader_canvas = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fcfbf7; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e6e3da; max-width: {zoom_level}px; margin: 0 auto;">
        
        <!-- Controls Toolbar System -->
        <div style="margin-bottom: 25px; display: flex; gap: 10px; align-items: center; border-bottom: 1px solid #e6e3da; padding-bottom: 15px;">
            <button id="btn-play" onclick="playAmazonReader()" style="padding: 10px 20px; background-color: #fad160; color: #111; border: 1px solid #e6b422; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 0.95rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">▶ Read Out Loud</button>
            <button id="btn-stop" onclick="stopAmazonReader()" style="padding: 10px 20px; background-color: #f0f2f6; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-weight: 500; font-size: 0.95rem;">⏸ Pause</button>
            <span id="speed-indicator" style="margin-left: auto; font-size: 0.85rem; color: #666; font-style: italic;">Amazon Tracking Status: Idle</span>
        </div>
        
        <!-- Book Page Display Area: Words wrap beautifully to mirror high-fidelity print grids -->
        <div id="kindle-text-grid" style="font-size: 1.35rem; line-height: 2.2rem; color: #222; text-align: justify; text-justify: inter-word; min-height: 450px; padding: 10px; letter-spacing: 0.3px; font-family: Georgia, serif;"></div>
    </div>

    <script>
        const originalTextString = "{js_safe_text}";
        const textGridContainer = document.getElementById("kindle-text-grid");
        const trackingStatus = document.getElementById("speed-indicator");
        
        // Break up the text page into individual targeting tokens
        const splitWordsArray = originalTextString.split(" ");
        
        # Format tokens into addressable span tags
        textGridContainer.innerHTML = splitWordsArray.map((word, idx) => `<span id="w-tok-${{idx}}" style="transition: background-color 0.1s ease, box-shadow 0.1s ease; padding: 2px 3px; margin: 0 1px; border-radius: 3px; display: inline-block;">${{word}}</span>`).join(" ");
        
        let browserVoiceSynth = window.speechSynthesis;
        let readingUtterance = null;
        
        function playAmazonReader() {{
            browserVoiceSynth.cancel();
            trackingStatus.innerText = "Amazon Tracking Status: Reading...";
            trackingStatus.style.color = "#2eb85c";
            
            readingUtterance = new SpeechSynthesisUtterance(originalTextString);
            readingUtterance.lang = 'en-US';
            readingUtterance.rate = 0.95; // Fluid, natural audiobook pacing
            
            // Core Dynamic Boundary Tracker Rule
            readingUtterance.onboundary = function(event) {{
                if (event.name === 'word') {{
                    const characterIndexOffset = event.charIndex;
                    const parsedTextSubstring = originalTextString.substring(0, characterIndexOffset).trim();
                    const activeWordTokenPointer = parsedTextSubstring ? parsedTextSubstring.split(" ").length : 0;
                    
                    // Wipe away all previous floating shadow blocks cleanly
                    document.querySelectorAll("#kindle-text-grid span").forEach(node => {{
                        node.style.backgroundColor = "transparent";
                        node.style.boxShadow = "none";
                        node.style.color = "#222";
                    }});
                    
                    // Project the smooth yellow focus shadow block directly over the targeted active line token
                    const activeNode = document.getElementById(`w-tok-${{activeWordTokenPointer}}`);
                    if (activeNode) {{
                        activeNode.style.backgroundColor = "#fff2a3"; // Authentic Amazon warm gold focus color
                        activeNode.style.boxShadow = "0 2px 6px #fff2a3, 0 -1px 3px #fff2a3"; 
                        activeNode.style.color = "#000";
                        
                        // Handle smooth scrolling if the page height stretches past viewport sizes
                        activeNode.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                    }}
                }}
            }};
            
            readingUtterance.onend = function() {{
                trackingStatus.innerText = "Amazon Tracking Status: Lesson Completed";
                trackingStatus.style.color = "#666";
                document.querySelectorAll("#kindle-text-grid span").forEach(node => {{
                    node.style.backgroundColor = "transparent";
                    node.style.boxShadow = "none";
                    node.style.color = "#222";
                }});
            }};
            
            browserVoiceSynth.speak(readingUtterance);
        }}
        
        function stopAmazonReader() {{
            browserVoiceSynth.cancel();
            trackingStatus.innerText = "Amazon Tracking Status: Paused";
            trackingStatus.style.color = "#dc3545";
        }}
    </script>
    """
    st.components.v1.html(amazon_reader_canvas, height=600, scrolling=False)

    # 6. Native Streamlit Layout Pagination Bar
    st.markdown("---")
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
    writer = PdfWriter()
    for p_idx in range(target_start - 1, target_end):
        if p_idx < len(reader.pages):
            writer.add_page(reader.pages[p_idx])
    
    full_chapter_buffer = io.BytesIO()
    writer.write(full_chapter_buffer)
    
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
