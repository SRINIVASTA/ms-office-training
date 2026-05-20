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
    
    # Accurate Chapter Index Mapping matching the structure of the training manual
    chapter_options = {
        "1. Microsoft Word (Pages 5 - 109)": {
            "start": 5, "end": 109, "label": "MS Word", "filename": "MS_Word_Training_Guide.pdf",
            "slides": [
                {"title": "Welcome to Word 2016", "desc": "Exploring the Quick Access Toolbar, Ribbon tabs, and workspace setup."},
                {"title": "Text Layout & Typography", "desc": "Mastering font adjustments, paragraphs, alignment, and formatting styles."},
                {"title": "Tables & Graphic Design", "desc": "How to insert tabular grids, style borders, and format illustrations safely."},
                {"title": "Document Finalization", "desc": "Managing page margins, page orientation, headers, footers, and print tracking."}
            ]
        },
        "2. Microsoft Excel (Pages 110 - 259)": {
            "start": 110, "end": 259, "label": "MS Excel", "filename": "MS_Excel_Training_Guide.pdf",
            "slides": [
                {"title": "Excel Interface & Cells", "desc": "Understanding rows, columns, unique cell addresses, and workbook navigation."},
                {"title": "Formulas & Basic Math", "desc": "Writing structural syntax using SUM, AVERAGE, COUNT, and standard operations."},
                {"title": "Data Sorting & Filters", "desc": "Organizing massive datasets alphabetically, numerically, or via custom filters."},
                {"title": "Charts & Visual Graphics", "desc": "Transforming clean data cells into standard Pie, Bar, and Line charts instantly."}
            ]
        },
        "3. Microsoft PowerPoint (Pages 260 - 323)": {
            "start": 260, "end": 323, "label": "MS PowerPoint", "filename": "MS_PowerPoint_Training_Guide.pdf",
            "slides": [
                {"title": "Slide Foundations", "desc": "Choosing structural layout designs, adding new slides, and placeholder control."},
                {"title": "Animations & Transitions", "desc": "Applying dynamic cinematic movements between slide deck switches cleanly."},
                {"title": "Media, Audio & Graphics", "desc": "Inserting external images, recording shapes, and adding media attachments."},
                {"title": "Delivering Presentations", "desc": "Using Presenter View, timeline controls, laser tools, and slide loops."}
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
    chapter_slides = chapter_options[selected_chapter]["slides"]
    total_pages = target_end - target_start + 1

    page_state_key = f"current_page_{chapter_name}"
    if page_state_key not in st.session_state:
        st.session_state[page_state_key] = 1

    # Progress Tracker Checkbox UI
    st.markdown("---")
    st.subheader("✅ Chapter Milestones")
    
    completed_count = 0
    for slide_item in chapter_slides:
        s_title = slide_item["title"]
        unique_key = f"{chapter_name}_{s_title}"
        is_checked = st.session_state.progress_tracker.get(unique_key, False)
        current_state = st.checkbox(s_title, value=is_checked, key=f"cb_{unique_key}")
        st.session_state.progress_tracker[unique_key] = current_state
        
        if current_state:
            completed_count += 1
            
    completion_rate = completed_count / len(chapter_slides) if chapter_slides else 0
    st.progress(completion_rate)
    st.write(f"Chapter Progress: {int(completion_rate * 100)}%")

    st.markdown("---")
    st.subheader("🔍 View Adjustments")
    zoom_level = st.slider("Adjust Viewer Width (px)", min_value=400, max_value=1400, value=1000, step=50)

# 4. Process and Display the PDF securely (PDF ON TOP)
try:
    reader = PdfReader("MS Office Reading Material.pdf")
    
    local_current_page = st.session_state[page_state_key]
    global_pdf_page = (target_start - 1) + (local_current_page - 1)
    
    # Safe rendering via raw data components to bypass Chrome Frame blocking bugs
    import base64
    writer = PdfWriter()
    if global_pdf_page < len(reader.pages):
        writer.add_page(reader.pages[global_pdf_page])
            
    chapter_pdf_buffer = io.BytesIO()
    writer.write(chapter_pdf_buffer)
    chapter_pdf_bytes = chapter_pdf_buffer.getvalue()
    base64_pdf = base64.b64encode(chapter_pdf_bytes).decode('utf-8')
    
    st.subheader(f"📖 Currently Viewing: {chapter_name}")
    st.info(f"Target Section: Page {target_start} to Page {target_end} ({total_pages} total training pages)")
    
    # Display the clear training page content frame
    pdf_display_style = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0" width="{zoom_level}px" height="600px" style="border:1px solid #ccc; border-radius:4px;"></iframe>'
    st.components.v1.html(pdf_display_style, height=610)
    
    st.markdown("---")
    
    # 5. Native Streamlit Page Scroller Controls (IN THE MIDDLE)
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
    
    # 6. FEATURE: Generated Video-Slideshow + Synced Shadow Voice Engine (VIDEO DOWN)
    st.subheader("📺 Generated Dynamic Lesson Presentation Player")
    
    active_page_object = reader.pages[global_pdf_page]
    extracted_raw_text = active_page_object.extract_text()
    clean_text = extracted_raw_text.replace("Srinivasta", "").strip() if extracted_raw_text else ""
    
    if clean_text:
        js_safe_text = clean_text.replace('"', '\\"').replace('\n', ' ')
        
        # Format our slide arrays into a clean JavaScript array literal
        import json
        js_slides_array = json.dumps(chapter_slides)
        
        # HTML5 + Canvas Presentation Player Component
        html_presentation_component = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e24; padding: 25px; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.3); color: white;">
            
            <!-- Controls Overlay Toolbar -->
            <div style="margin-bottom: 20px; display: flex; gap: 10px;">
                <button id="btn-play" onclick="startLessonVideo()" style="padding: 10px 20px; background-color: #2eb85c; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s;">▶ Play Lesson</button>
                <button id="btn-stop" onclick="stopLessonVideo()" style="padding: 10px 20px; background-color: #e55353; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s;">⏹ Pause Lesson</button>
            </div>
            
            <!-- Audio Voice Box containing Text Shadows -->
            <div id="shadow-text-screen" style="font-size: 1.1rem; line-height: 1.8rem; color: #fff; margin-bottom: 20px; max-height: 90px; overflow-y: auto; background: #2a2a35; padding: 12px; border-left: 5px solid #321fdb; border-radius: 4px; box-sizing: border-box;"></div>
            
            <!-- Generated Presentation Video Canvas Deck -->
            <div id="video-canvas-deck" style="background: linear-gradient(135deg, #321fdb 0%, #1f1487 100%); height: 350px; border-radius: 8px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px; text-align: center; box-shadow: inset 0 0 40px rgba(0,0,0,0.5); transition: all 0.5s ease;">
                <h1 id="slide-title" style="font-size: 2.8rem; margin: 0 0 15px 0; font-weight: 700; text-shadow: 2px 4px 10px rgba(0,0,0,0.4); letter-spacing: 1px;">Ready to Begin</h1>
                <p id="slide-desc" style="font-size: 1.4rem; max-width: 600px; line-height: 2rem; color: #ebedef; text-shadow: 1px 2px 5px rgba(0,0,0,0.3);">Click 'Play Lesson' to start the voice tracking and visual animation deck.</p>
            </div>
        </div>

        <script>
            const textToRead = "{js_safe_text}";
            const textBox = document.getElementById("shadow-text-screen");
            const slideTitle = document.getElementById("slide-title");
            const slideDesc = document.getElementById("slide-desc");
            const canvasDeck = document.getElementById("video-canvas-deck");
            
            const slidesData = {js_slides_array};
            const wordsArray = textToRead.split(" ");
            textBox.innerHTML = wordsArray.map((word, idx) => `<span id="word-${{idx}}">${{word}}</span>`).join(" ");
            
            let synth = window.speechSynthesis;
            let utterance = null;
            const totalWords = wordsArray.length;

            // Beautiful fluid background color gradients to simulate dynamic video transitions
            const dynamicGradients = [
                "linear-gradient(135deg, #321fdb 0%, #1f1487 100%)",   // Royal Blue
                "linear-gradient(135deg, #2eb85c 0%, #1b6d37 100%)",   // Office Green
                "linear-gradient(135deg, #f9b115 0%, #9b6d03 100%)",   // Warning Amber
                "linear-gradient(135deg, #636f83 0%, #2f3542 100%)"    // Premium Platinum Charcoal
            ];
            
            function startLessonVideo() {{
                synth.cancel();
                
                utterance = new SpeechSynthesisUtterance(textToRead);
                utterance.lang = 'en-US';
                utterance.rate = 0.95; // Clear corporate voice training pace
                
                utterance.onboundary = function(event) {{
                    if (event.name === 'word') {{
                        const charIndex = event.charIndex;
                        const textUpToChar = textToRead.substring(0, charIndex).trim();
                        const currentWordIdx = textUpToChar ? textUpToChar.split(" ").length : 0;
                        
                        // 1. Refresh shadow tracker highlights
                        document.querySelectorAll("#shadow-text-screen span").forEach(span => {{
                            span.style.backgroundColor = "transparent";
                            span.style.color = "#fff";
                        }});
                        
                        const activeWordSpan = document.getElementById(`word-${{currentWordIdx}}`);
                        if (activeWordSpan) {{
                            activeWordSpan.style.backgroundColor = "#f9b115";
                            activeWordSpan.style.color = "#000";
                            activeWordSpan.style.borderRadius = "3px";
                        }}
                        
                        // 2. AUTOMATIC PRESENTATION VIDEO SLIDE FLIPPING
                        // Calculates location ratio and automatically matches text to slide themes
                        const completionRatio = currentWordIdx / totalWords;
                        let slideTargetIdx = Math.floor(completionRatio * slidesData.length);
                        if (slideTargetIdx >= slidesData.length) slideTargetIdx = slidesData.length - 1;
                        
                        // Dynamically morph the slide visual parameters seamlessly
                        if(slidesData[slideTargetIdx]) {{
                            slideTitle.innerText = slidesData[slideTargetIdx].title;
                            slideDesc.innerText = slidesData[slideTargetIdx].desc;
                            canvasDeck.style.background = dynamicGradients[slideTargetIdx % dynamicGradients.length];
                        }}
                    }}
                }};
                
                utterance.onend = function() {{
                    document.querySelectorAll("#shadow-text-screen span").forEach(span => {{
                        span.style.backgroundColor = "transparent";
                    }});
                    slideTitle.innerText = "Lesson Completed!";
                    slideDesc.innerText = "Excellent tracking momentum. Click 'Next Page' or advance to your next milestone checklist item.";
                    canvasDeck.style.background = "linear-gradient(135deg, #463077 0%, #251742 100%)";
                }};
                
                synth.speak(utterance);
            }}
            
            function stopLessonVideo() {{
                synth.cancel();
            }}
        </script>
        """
        st.components.v1.html(html_presentation_component, height=600, scrolling=False)
    else:
        st.caption("ℹ️ No textual content exists on this layout page to power the automation presentation video deck.")

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
