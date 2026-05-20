import io
import streamlit as st
from pypdf import PdfReader, PdfWriter
from streamlit_pdf_viewer import pdf_viewer

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
    
    # VERIFIED CHAPTER MAPPING WITH TIMESTAMPS: Added "video_url" and section "seconds" for tracking
    chapter_options = {
        "1. Microsoft Word (Pages 5 - 109)": {
            "start": 5, "end": 109, "label": "MS Word", "filename": "MS_Word_Training_Guide.pdf",
            "video_url": "https://w3schools.com", # Replace with your actual Word video MP4 link
            "sections": [
                {"name": "Word Basics & Interface", "seconds": 0},
                {"name": "Text Formatting & Styles", "seconds": 15},
                {"name": "Tables & Graphics", "seconds": 30},
                {"name": "Page Layout & Printing", "seconds": 45}
            ]
        },
        "2. Microsoft Excel (Pages 110 - 259)": {
            "start": 110, "end": 259, "label": "MS Excel", "filename": "MS_Excel_Training_Guide.pdf",
            "video_url": "https://w3schools.com", # Replace with your actual Excel video MP4 link
            "sections": [
                {"name": "Excel Spreadsheet Basics", "seconds": 0},
                {"name": "Formulas & Basic Functions", "seconds": 20},
                {"name": "Data Sorting & Filtering", "seconds": 40},
                {"name": "Charts & Graphs", "seconds": 60}
            ]
        },
        "3. Microsoft PowerPoint (Pages 260 - 323)": {
            "start": 260, "end": 323, "label": "MS PowerPoint", "filename": "MS_PowerPoint_Training_Guide.pdf",
            "video_url": "https://w3schools.com", # Replace with your actual PowerPoint video MP4 link
            "sections": [
                {"name": "Presentation Basics & Layouts", "seconds": 0},
                {"name": "Adding Animations & Transitions", "seconds": 10},
                {"name": "Inserting Media & Objects", "seconds": 25},
                {"name": "Slide Show Delivery", "seconds": 50}
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
    active_video_url = chapter_options[selected_chapter]["video_url"]
    total_pages = target_end - target_start + 1

    page_state_key = f"current_page_{chapter_name}"
    if page_state_key not in st.session_state:
        st.session_state[page_state_key] = 1

    # Progress Tracker Checkbox UI
    st.markdown("---")
    st.subheader("✅ Chapter Milestones")
    
    completed_count = 0
    for section_obj in chapter_sections:
        s_name = section_obj["name"]
        unique_key = f"{chapter_name}_{s_name}"
        is_checked = st.session_state.progress_tracker.get(unique_key, False)
        current_state = st.checkbox(s_name, value=is_checked, key=f"cb_{unique_key}")
        st.session_state.progress_tracker[unique_key] = current_state
        
        if current_state:
            completed_count += 1
            
    completion_rate = completed_count / len(chapter_sections) if chapter_sections else 0
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
    
    writer = PdfWriter()
    if global_pdf_page < len(reader.pages):
        writer.add_page(reader.pages[global_pdf_page])
            
    chapter_pdf_buffer = io.BytesIO()
    writer.write(chapter_pdf_buffer)
    chapter_pdf_bytes = chapter_pdf_buffer.getvalue()
    
    st.subheader(f"📖 Currently Viewing: {chapter_name}")
    st.info(f"Target Section: Page {target_start} to Page {target_end} ({total_pages} total training pages)")
    
    # Render the PDF viewport on top
    pdf_viewer(
        input=chapter_pdf_bytes,
        width=zoom_level,
        key=f"pdf_render_{chapter_name}_{local_current_page}"
    )
    
    st.markdown("---")
    
    # 5. Native Streamlit Page Scroller & Input Navigation Row (IN THE MIDDLE)
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
    
    # 6. FEATURE: Combined Synced Shadow Reader + Video Player Component (VIDEO DOWN)
    st.subheader("🔊 Synced Guided Reading & Video Tutorial")
    
    active_page_object = reader.pages[global_pdf_page]
    extracted_raw_text = active_page_object.extract_text()
    clean_text = extracted_raw_text.replace("Srinivasta", "").strip() if extracted_raw_text else ""
    
    if clean_text:
        js_safe_text = clean_text.replace('"', '\\"').replace('\n', ' ')
        
        # Determine timeline jumping constraints based on milestones
        current_page_milestones = [s for s in chapter_sections]
        
        # Build layout holding text box at top, and video matching directly below it
        html_speech_video_component = f"""
        <div style="font-family: sans-serif; background-color: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #ddd;">
            
            <!-- Controls -->
            <div style="margin-bottom: 15px;">
                <button id="btn-play" onclick="startReadingAndVideo()" style="padding: 8px 16px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-right: 10px;">▶ Play Lesson</button>
                <button id="btn-stop" onclick="stopEverything()" style="padding: 8px 16px; background-color: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;"> Tap to Pause / Mute</button>
            </div>
            
            <!-- Shadow Follow Text Frame -->
            <div id="reading-text-box" style="font-size: 1.1rem; line-height: 1.7rem; color: #333; margin-bottom: 20px; max-height: 120px; overflow-y: auto; background: white; padding: 10px; border: 1px solid #eee; border-radius: 4px;"></div>
            
            <!-- Integrated Video Player Display (Down Below) -->
            <div style="text-align: center;">
                <video id="lesson-video" width="100%" max-width="720" height="400" controls style="border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                    <source src="{active_video_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>

        <script>
            const textToRead = "{js_safe_text}";
            const textBox = document.getElementById("reading-text-box");
            const videoPlayer = document.getElementById("lesson-video");
            
            const wordsArray = textToRead.split(" ");
            textBox.innerHTML = wordsArray.map((word, idx) => `<span id="word-${{idx}}">${{word}}</span>`).join(" ");
            
            let synth = window.speechSynthesis;
            let utterance = null;
            
            // Approximate total words length calculation to distribute video jump speeds evenly
            const totalWordsCount = wordsArray.length;
            const videoDurationPlaceholder = 60; // fallback duration matrix baseline
            
            function startReadingAndVideo() {{
                synth.cancel();
                videoPlayer.play();
                
                utterance = new SpeechSynthesisUtterance(textToRead);
                utterance.lang = 'en-US';
                utterance.rate = 0.95; // Slightly metered natural rhythm pacing
                
                utterance.onboundary = function(event) {{
                    if (event.name === 'word') {{
                        const charIndex = event.charIndex;
                        const textUpToChar = textToRead.substring(0, charIndex).trim();
                        const wordCountIndex = textUpToChar ? textUpToChar.split(" ").length : 0;
                        
                        // 1. Core Shadow updates
                        document.querySelectorAll("#reading-text-box span").forEach(span => {{
                            span.style.backgroundColor = "transparent";
                            span.style.boxShadow = "none";
                        }});
                        
                        const activeWordSpan = document.getElementById(`word-${{wordCountIndex}}`);
                        if (activeWordSpan) {{
                            activeWordSpan.style.backgroundColor = "#ffeb3b";
                            activeWordSpan.style.boxShadow = "0px 0px 6px #ffeb3b";
                            activeWordSpan.style.borderRadius = "3px";
                        }}
                        
                        // 2. DYNAMIC VIDEO SYNCING
                        // Calculate how far along the text reader is, and sync the video playhead
                        if(videoPlayer.duration) {{
                            const percentageRead = wordCountIndex / totalWordsCount;
                            const targetVideoTime = videoPlayer.duration * percentageRead;
                            
                            // Prevent tiny micro-stutters by updating playhead only when needed
                            if (Math.abs(videoPlayer.currentTime - targetVideoTime) > 3) {{
                                videoPlayer.currentTime = targetVideoTime;
                            }}
                        }}
                    }}
                }};
                
                utterance.onend = function() {{
                    videoPlayer.pause();
                    document.querySelectorAll("#reading-text-box span").forEach(span => {{
                        span.style.backgroundColor = "transparent";
                        span.style.boxShadow = "none";
                    }});
                }};
                
                synth.speak(utterance);
            }}
            
            function stopEverything() {{
                synth.cancel();
                videoPlayer.pause();
            }}
        </script>
        """
        st.components.v1.html(html_speech_video_component, height=620, scrolling=True)
    else:
        st.caption("ℹ️ No text found to drive the synchronized layout reader.")

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
