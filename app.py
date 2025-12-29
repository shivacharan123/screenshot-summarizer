import streamlit as st
from PIL import Image, UnidentifiedImageError
import tempfile
import os
import time
from datetime import datetime
from pathlib import Path

# Placeholder for your custom utils
from ocr_utils import extract_text
from llm_utils import summarize_text

# -------------------------------------------------
# 🎨 UI CONFIGURATION & STYLING
# -------------------------------------------------
st.set_page_config(
    page_title="VisionInsight | Pro Summarizer",
    page_icon="📑",
    layout="wide"  # Professional dashboards use wide layout
)

# Custom CSS for a refined look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #007bff;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #007bff;
        color: white;
        transform: translateY(-2px);
    }
    div[data-testid="stMetricContainer"] {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# ✨ DYNAMIC GREETING LOGIC
# -------------------------------------------------
def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good Morning"
    elif hour < 17: return "Good Afternoon"
    else: return "Good Evening"

# -------------------------------------------------
# 🛠️ CORE FUNCTIONS
# -------------------------------------------------
SCREENSHOT_DIR = Path(r"C:\Users\shiva\OneDrive\Pictures\Screenshots")

def safe_load_image(path, retries=3, delay=0.5):
    for _ in range(retries):
        try:
            return Image.open(path).convert("RGB")
        except UnidentifiedImageError:
            time.sleep(delay)
    return None

def get_latest_screenshot():
    images = list(SCREENSHOT_DIR.glob("*.png")) + list(SCREENSHOT_DIR.glob("*.jpg"))
    if not images: return None
    return max(images, key=lambda p: p.stat().st_mtime)

# -------------------------------------------------
# 🛰️ SESSION STATE
# -------------------------------------------------
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "last_processed" not in st.session_state: st.session_state.last_processed = None

# -------------------------------------------------
# 🏢 SIDEBAR / HEADER
# -------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3421/3421102.png", width=100)
    st.title("VisionInsight AI")
    st.markdown("---")
    mode = st.radio(
        "🛠️ Work Mode",
        ["📂 Auto-Scan Local", "📤 Manual Upload"],
        help="Choose how you want to ingest the screenshot."
    )
    st.info("💡 Tip: Press `Win + Shift + S` to take a screenshot, then click Scan.")

# -------------------------------------------------
# 🏠 MAIN INTERFACE
# -------------------------------------------------
col_title, col_time = st.columns([3, 1])
with col_title:
    st.title(f"☀️ {get_greeting()}, Shiva")
    st.caption("Intelligence engine for rapid screenshot analysis and document synthesis.")

# Metrics Row
m1, m2, m3 = st.columns(3)
m1.metric("Status", "Ready", "Optimal")
m2.metric("Intelligence", "GPT-4o / OCR-v2")
m3.metric("Storage", "Local Sync" if "Auto-Scan" in mode else "Cloud Temp")

st.divider()

# Logic for Content
image_to_process = None
source_path = None

if "Auto-Scan" in mode:
    if st.button("🔍 Sync Latest Capture", use_container_width=True):
        latest = get_latest_screenshot()
        if latest:
            source_path = str(latest)
            image_to_process = safe_load_image(source_path)
            st.session_state.last_processed = source_path
        else:
            st.warning("No screenshots detected in your system folder.")
else:
    uploaded_file = st.file_uploader("Drop professional document/screenshot here", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image_to_process = Image.open(uploaded_file).convert("RGB")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            image_to_process.save(tmp.name)
            source_path = tmp.name

# -------------------------------------------------
# 📊 ANALYSIS VIEW
# -------------------------------------------------
if image_to_process:
    view_col, data_col = st.columns([1, 1], gap="large")
    
    with view_col:
        st.subheader("🖼️ Source Image")
        st.image(image_to_process, use_container_width=True)
    
    with data_col:
        with st.status("🚀 Processing Document...", expanded=True) as status:
            st.write("Extracting raw text via OCR...")
            raw_text = extract_text(source_path)
            
            st.write("Synthesizing key insights...")
            summary_result = summarize_text(raw_text)
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # Tabs for better organization
        tab1, tab2 = st.tabs(["📌 Executive Summary", "📝 Raw Data"])
        
        with tab1:
            st.success("**Key Highlights**")
            st.write(summary_result)
        
        with tab2:
            st.text_area("OCR Extraction Output", value=raw_text, height=300)

    # 💬 CHAT INTERFACE AT BOTTOM
    st.divider()
    st.subheader("💬 Ask Questions about this Data")
    
    # Display chat history
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    if user_query := st.chat_input("Ask: 'What are the main dates mentioned?'"):
        st.session_state.chat_history.append(("user", user_query))
        with st.chat_message("user"):
            st.write(user_query)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full_context = f"Text: {raw_text}\nSummary: {summary_result}\nUser Question: {user_query}"
                response = summarize_text(full_context) # Using your LLM function
                st.write(response)
                st.session_state.chat_history.append(("assistant", response))

# -------------------------------------------------
# 🏷️ FOOTER
# -------------------------------------------------
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; color: #6c757d; border-top: 1px solid #dee2e6;'>
        VisionInsight Professional v1.0 | Standardized Reporting Engine
    </div>
    """, unsafe_allow_html=True)