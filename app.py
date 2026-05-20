import io
import streamlit as st
from pypdf import PdfReader, PdfWriter

# 1. Universal Layout Settings
st.set_page_config(
    page_title="MS Office 2016: Complete Training Guide",
    page_icon="📚",
    layout="wide"
)

# Initialize persistent session state for progress tracking & quizzes
if "progress_tracker" not in st.session_state:
    st.session_state.progress_tracker = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# 2. Page Headers
st.title("📚 MS Office 2016: Complete Training Guide")
st.caption("A foundational training manual by Srinivasta — open to learners of all ages.")

# 3. Interactive Chapter Selection & Page Math
with st.sidebar:
    st.header("📖 Navigation Controls")
    
    chapter_options = {
        "1. Microsoft Word (Pages 5 - 109)": {
            "start": 5, "end": 109, "label": "MS Word", "filename": "MS_Word_Training_Guide.pdf",
            "sections": ["Word Basics & Interface", "Text Formatting & Styles", "Tables & Graphics", "Page Layout & Printing"],
            "quiz": [
                {"q": "Which tab in MS Word 2016 contains the font formatting options?", "options": ["Insert", "Home", "Layout", "Review"], "correct": "Home"},
                {"q": "What is the default extension for a saved MS Word 2016 file?", "options": [".txt", ".docx", ".pdf", ".xlsx"], "correct": ".docx"}
            ]
        },
        "2. Microsoft Excel (Pages 110 - 259)": {
            "start": 110, "end": 259, "label": "MS Excel", "filename": "MS_Excel_Training_Guide.pdf",
            "sections": ["Excel Spreadsheet Basics", "Formulas & Basic Functions", "Data Sorting & Filtering", "Charts & Graphs"],
            "quiz": [
                {"q": "Which formula correctly adds cells A1 and A2 in Excel?", "options": ["=ADD(A1:A2)", "=SUM(A1,A2)", "=A1+A2", "Both =SUM(A1,A2) and =A1+A2"], "correct": "Both =SUM(A1,A2) and =A1+A2"},
                {"q": "What is the intersection of a row and a column called?", "options": ["Grid", "Block", "Cell", "Sheet"], "correct": "Cell"}
            ]
        },
        "3. Microsoft PowerPoint (Pages 260 - 323)": {
            "start": 260, "end": 323, "label": "MS PowerPoint", "filename": "MS_PowerPoint_Training_Guide.pdf",
            "sections": ["Presentation Basics & Layouts", "Adding Animations & Transitions", "Inserting Media & Objects", "Slide Show Delivery"],
            "quiz": [
                {"q": "What is the shortcut key to start a presentation slide show from the beginning?", "options": ["F5", "Ctrl + P", "Spacebar", "F11"], "correct": "F5"},
                {"q": "Which effect controls how a single slide moves off the screen and the next one appears?", "options": ["Animation", "Transition", "Wipe", "Fade"], "correct": "Transition"}
            ]
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
    chapter_quiz = chapter_options[selected_chapter]["quiz"]
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
    zoom_level = st.slider("Adjust Document Size (px width)", min_value=400, max_value=1400, value=900, step=50)

# 4. Process and Display the PDF Securely via Native Streamlit API Layer
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
    
    # Renders original graphic manual safely on top layer (Unblockable by Chrome)
    st.pdf(chapter_pdf_bytes)

    # 5. HYBRID VOICE AND TRACKING SHADOW ACCESS CONTAINER
    st.markdown("---")
    st.subheader("🔊 Kindle-Style Tracking Shadow Text Assistant")
    
    active_page_object = reader.pages[global_pdf_page]
    extracted_raw_text = active_page_object.extract_text()
    
    clean_text = extracted_raw_text.replace("Srinivasta", "").strip() if extracted_raw_text else ""
    js_safe_text = clean_text.replace('"', '\\"').replace('\n', ' ') if clean_text else "No text content discovered on this page."
    
    html_tracking_component = f"""
    <div style="font-family: 'Segoe UI', system-ui, sans-serif; background-color: #fcfbf7; padding: 25px; border-radius: 8px; border: 1px solid #e6e3da;">
        <div style="margin-bottom: 20px; display: flex; gap: 10px; align-items: center;">
            <button id="btn-play" onclick="startAutomatedReading()" style="padding: 10px 22px; background-color: #fad160; color: #111; border: 1px solid #e6b422; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 0.95rem;">▶ Read Out Loud</button>
            <button id="btn-stop" onclick="stopAutomatedReading()" style="padding: 10px 22px; background-color: #f0f2f6; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-weight: 500; font-size: 0.95rem;">⏸ Pause</button>
            <span id="reading-tracker-status" style="margin-left: auto; font-size: 0.85rem; color: #666; font-weight: 500;">Status: Ready to assist</span>
        </div>
        <div id="accessible-text-deck" style="font-size: 1.25rem; line-height: 2.1rem; color: #222; text-align: justify; font-family: Georgia, serif; max-height: 200px; overflow-y: auto; background: white; padding: 15px; border: 1px solid #eee; border-radius: 4px;"></div>
    </div>

    <script>
        const textPayload = "{js_safe_text}";
        const textDeck = document.getElementById("accessible-text-deck");
        const trackingStatus = document.getElementById("reading-tracker-status");
        
        const textWordsArray = textPayload.split(" ");
        textDeck.innerHTML = textWordsArray.map((word, idx) => `<span id="word-token-${{idx}}" style="padding: 1px 3px; margin: 0 1px; border-radius: 3px; transition: all 0.05s ease;">${{word}}</span>`).join(" ");
        
        let speechEngine = window.speechSynthesis;
        let utterInstance = null;
        
        function startAutomatedReading() {{
            speechEngine.cancel();
            trackingStatus.innerText = "Status: Highlighting Tracking Cursor...";
            trackingStatus.style.color = "#2eb85c";
            
            utterInstance = new SpeechSynthesisUtterance(textPayload);
            utterInstance.lang = 'en-US';
            utterInstance.rate = 0.95;
            
            utterInstance.onboundary = function(event) {{
                if (event.name === 'word') {{
                    const characterOffset = event.charIndex;
                    const runningSubstring = textPayload.substring(0, characterOffset).trim();
                    const activeWordIndexPointer = runningSubstring ? runningSubstring.split(" ").length : 0;
                    
                    document.querySelectorAll("#accessible-text-deck span").forEach(node => {{
                        node.style.backgroundColor = "transparent";
                        node.style.boxShadow = "none";
                    }});
                    
                    const targetedNode = document.getElementById(`word-token-${{activeWordIndexPointer}}`);
                    if (targetedNode) {{
                        targetedNode.style.backgroundColor = "#fff2a3";
                        targetedNode.style.boxShadow = "0 1px 5px #fff2a3";
                        targetedNode.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                    }}
                }}
            }};
            
            utterInstance.onend = function() {{
                trackingStatus.innerText = "Status: Reading Completed";
                trackingStatus.style.color = "#666";
                document.querySelectorAll("#accessible-text-deck span").forEach(node => {{
                    node.style.backgroundColor = "transparent";
                }});
            }};
            
            speechEngine.speak(utterInstance);
        }}
        
        function stopAutomatedReading() {{
            speechEngine.cancel();
            trackingStatus.innerText = "Status: Paused";
            trackingStatus.style.color = "#dc3545";
        }}
    </script>
    """
    st.components.v1.html(html_tracking_component, height=300, scrolling=False)

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
            f"<h3 style='text-align: center; margin:0;'>📄 Page {local_current_page} of {total_pages}</h3>"
            f"<p style='text-align: center; color: gray; margin:0;'>(Manual Page: {target_start + local_current_page - 1})</p>", 
            unsafe_allow_html=True
        )
        
    with col3:
        st.write("") 
        if st.button("Next Page ➡️", use_container_width=True):
            if st.session_state[page_state_key] < total_pages:
                st.session_state[page_state_key] += 1
                st.rerun()

    # 7. NEW FEATURE: INTERACTIVE CHAPTER QUIZ SECTION
    st.markdown("---")
    st.header(f"📝 Interactive Mini-Quiz: {chapter_name}")
    st.caption("Test your understanding of this software block before downloading your files.")
    
    quiz_form_key = f"quiz_form_{chapter_name}"
    score = 0
    
    with st.form(key=quiz_form_key):
        user_selections = {}
        for idx, item in enumerate(chapter_quiz):
            st.markdown(f"**Q{idx+1}: {item['q']}**")
            user_selections[idx] = st.radio(
                "Select the correct option:",
                options=item["options"],
                key=f"q_{chapter_name}_{idx}"
            )
            st.markdown("")
            
        submit_quiz = st.form_submit_button("Submit Quiz Answers", type="secondary")
        
        if submit_quiz:
            for idx, item in enumerate(chapter_quiz):
                if user_selections[idx] == item["correct"]:
                    score += 1
                    st.success(f"✔️ Q{idx+1} is Correct!")
                else:
                    st.error(f"❌ Q{idx+1} is Incorrect. Correct answer: {item['correct']}")
            
            st.metric(label="Your Quiz Score", value=f"{score} / {len(chapter_quiz)}")
            if score == len(chapter_quiz):
                st.balloons()

    st.markdown("---")
    
    # 8. Chapter Manual Download Action Button
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
