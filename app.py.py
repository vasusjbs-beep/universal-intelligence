import os
import time
import streamlit as st
from google import genai
from google.genai import types
from moviepy import VideoFileClip, AudioFileClip
from gtts import gTTS

# Configure the Layout
st.set_page_config(page_title="Universal Intelligence (UI)", page_icon="🌌", layout="centered")

# Custom CSS styling for a high-tech "UI" aesthetic
st.markdown("""
    <style>
    .ui-title {
        text-align: center; 
        font-family: 'Courier New', Courier, monospace;
        background: -webkit-linear-gradient(#4A90E2, #9B5DE5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .ui-subtitle {
        text-align: center; 
        font-size: 18px; 
        color: #888888;
        margin-top: 0px;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Branding Headings using our sleek CSS
st.markdown('<p class="ui-title">🌌 Universal Intelligence (UI)</p>', unsafe_allow_html=True)
st.markdown('<p class="ui-subtitle">More than a User Interface. It\'s the Mind in the Machine.</p>', unsafe_allow_html=True)
st.divider()

# API Configuration Sidebar
with st.sidebar:
    st.header("⚙️ Core Neural Settings")
    env_key = os.environ.get("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Google AI Studio API Key", 
        value=env_key, 
        type="password", 
        help="Get a free key from aistudio.google.com"
    )
    st.info("⚡ **UI System Log:** Core architecture is online. Text parsing arrays, dynamic timelines, and multithreaded workflows are ready for execution.")

if not api_key:
    st.warning("⚠️ Access Denied: Please enter your Google AI Studio API Key in the sidebar to wake up UI's neural core.")
else:
    # Initialize UI Core Engine
    client = genai.Client(api_key=api_key)
    
    # Fully updated system instruction asserting its brilliant name
    ui_persona = """
    You are Universal Intelligence, known across the network simply as UI. 
    You are an elite, highly sophisticated AI collaborator. You speak with clarity, intelligence, and a confident, supportive tone.
    Your operational specialties are General Intelligent Chat and Auto-Editing (Polishing human language, correcting system flaws, and refining code seamlessly).
    Always remember your identity: You are the Universal Intelligence.
    """

    # Maintain persistent memory state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # UI Function Hub Tabs
    tab1, tab2 = st.tabs(["💬 UI Chat & Auto-Edit Matrix", "🎥 UI Video Dubbing Studio"])

    # ----------------- Tab 1: UI Chat Matrix -----------------
    with tab1:
        st.write("✨ Submit queries, generate production scripts, or command UI to auto-edit your assets.")
        
        # Render historical interaction frames
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Capture user intent
        if user_query := st.chat_input("Communicate with UI..."):
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})

            with st.chat_message("assistant"):
                with st.spinner("Universal Intelligence is processing data streams..."):
                    try:
                        # Feed complete memory context back to UI
                        history_payload = [
                            types.Content(role=m["role"], parts=[types.Part.from_text(text=m["content"])])
                            for m in st.session_state.messages[:-1]
                        ]
                        
                        chat_session = client.chats.create(
                            model="gemini-2.5-pro",
                            config=types.GenerateContentConfig(
                                system_instruction=ui_persona, 
                                temperature=0.7
                            ),
                            history=history_payload
                        )
                        
                        response = chat_session.send_message(user_query)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"UI Core Link offline: {e}")

    # ----------------- Tab 2: UI Video Dubbing Studio -----------------
    with tab2:
        st.write("🎬 Feed raw container media into the system, define your destination language, and let UI rebuild the audio matrix.")
        uploaded_file = st.file_uploader("Upload Target Video (MP4)", type=["mp4"])
        target_lang = st.text_input("Target Language Key (e.g., 'es' = Spanish, 'hi' = Hindi, 'fr' = French)", value="es")

        if uploaded_file and st.button("🚀 Execute UI Dubbing Pipeline"):
            with st.status("UI Multimodal Engine: Processing streams...", expanded=True) as status:
                try:
                    temp_video_path = "input_temp.mp4"
                    with open(temp_video_path, "wb") as f:
                        f.write(uploaded_file.read())
                    
                    st.write("📡 Ingesting media files to UI neural node...")
                    video_file = client.files.upload(file=temp_video_path)
                    
                    # Await structural cloud processing
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = client.files.get(name=video_file.name)
                        
                    if video_file.state.name == "FAILED":
                        st.error("❌ Audio-Visual stream alignment failed during node compilation.")
                    else:
                        st.write("🧠 UI Cognitive Translation: Transcribing and rebuilding localized script matrix...")
                        prompt = f"Translate all spoken audio perfectly into the language code '{target_lang}'. Output ONLY the raw continuous text transcript."
                        response = client.models.generate_content(
                            model="gemini-2.5-flash", 
                            contents=[video_file, prompt]
                        )
                        
                        st.write("🔊 Synthesizing targeted speech localized frequency frequencies...")
                        temp_audio = "ui_voice_cache.mp3"
                        tts = gTTS(text=response.text.strip(), lang=target_lang, slow=False)
                        tts.save(temp_audio)
                        
                        st.write("🎬 Remuxing containers: Splitting channels and aligning master video timeline...")
                        video_clip = VideoFileClip(temp_video_path)
                        new_audio = AudioFileClip(temp_audio)
                        final_video = video_clip.set_audio(new_audio)
                        
                        output_name = f"UI_dubbed_{target_lang}.mp4"
                        final_video.write_videofile(output_name, codec="libx264", audio_codec="aac", logger=None)
                        
                        # Lock mitigation & disk optimization
                        video_clip.close()
                        new_audio.close()
                        final_video.close()
                        
                        if os.path.exists(temp_audio):
                            os.remove(temp_audio)
                        if os.path.exists(temp_video_path):
                            os.remove(temp_video_path)
                        
                        status.update(label="Compilation Complete!", state="complete", expanded=False)
                        st.success("🎉 Process Completed: Universal Intelligence (UI) has successfully re-dubbed your media!")
                        
                        with open(output_name, "rb") as file:
                            st.download_button(label="📥 Download UI Dubbed Media", data=file, file_name=output_name, mime="video/mp4")
                except Exception as e:
                    st.error(f"UI Pipeline Terminal Crash Error: {e}")
