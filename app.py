import os
import base64
from pathlib import Path
from io import BytesIO

from dotenv import load_dotenv
import streamlit as st

from meeting_core import transcribe_audio, analyze_meeting, pretty_action_items

# --------- Helper to build markdown export ---------
def build_markdown_export(transcript: str, insights: dict) -> str:
    lines = []
    lines.append("# 💡 Meeting Whisperer Notes\n")
    lines.append("## Summary\n")
    lines.append(insights.get("summary", "") + "\n")

    lines.append("## Decisions\n")
    for d in insights.get("decisions", []):
        lines.append(f"- {d}")
    lines.append("")

    lines.append("## Action Items\n")
    lines.append(pretty_action_items(insights.get("action_items", [])))
    lines.append("")

    lines.append("## Risks & Open Questions\n")
    for r in insights.get("risks_open_questions", []):
        lines.append(f"- {r}")
    lines.append("")

    lines.append("## Full Transcript\n")
    lines.append("```")
    lines.append(transcript)
    lines.append("```")

    return "\n".join(lines)

# --------- Page config MUST be first Streamlit call ---------
st.set_page_config(
    page_title="Meeting Whisperer",
    page_icon="💡",
    layout="wide"
)

# --------- Background image ---------
def add_background(image_path: str):
    image_file = Path(image_path)
    if not image_file.exists():
        st.warning(f"Background image not found: {image_path}")
        return

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

add_background("Assets/background.jpg")

# --------- Setup / API key ---------
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("Please set OPENAI_API_KEY in a .env or environment variable.")
    st.stop()

# --------- Sidebar ---------
st.sidebar.title("💡 Meeting Whisperer")
st.sidebar.markdown(
    "Upload a recording of your meeting and get a clean summary, "
    "decisions, and action items."
)
temperature = st.sidebar.slider("Creativity (for wording only)", 0.0, 1.0, 0.2)

# --------- Main layout ---------
st.title("💡 Meeting Whisperer")
st.caption("Turn messy meetings into clean notes and action items.")

# --- Demo audio controls ---
DEMO_AUDIO_PATH = Path("Assets/demo_audio.mp3")

with st.expander("🎧 Demo audio (for recruiters)", expanded=True):
    cols = st.columns([1, 1, 2])
    with cols[0]:
        use_demo = st.button("Use demo audio", type="secondary", use_container_width=True)
    with cols[1]:
        if DEMO_AUDIO_PATH.exists():
            demo_bytes = DEMO_AUDIO_PATH.read_bytes()
            st.download_button(
                "Download demo audio",
                data=demo_bytes,
                file_name="meeting_whisperer_demo.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )
        else:
            st.caption("Add Assets/demo_audio.mp3 to enable demo.")

# --- Upload area ---
uploaded_file = st.file_uploader(
    "Upload audio (mp3, wav, m4a, etc.)",
    type=["mp3", "wav", "m4a", "mp4", "mpeg", "ogg"]
)

# --- Decide which audio to use ---
file_bytes = None
filename = None

if use_demo and DEMO_AUDIO_PATH.exists():
    file_bytes = DEMO_AUDIO_PATH.read_bytes()
    filename = DEMO_AUDIO_PATH.name
    st.success("Demo audio loaded. Click **Transcribe & Analyze**.")
elif uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()   # ✅ don't consume stream
    filename = uploaded_file.name

# Preview audio
if file_bytes is not None:
    st.audio(file_bytes)

    if st.button("Transcribe & Analyze", type="primary"):
        # --- Transcription ---
        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(
                file_bytes=file_bytes,
                filename=filename
            )

        # --- Transcript ---
        st.subheader("📝 Transcript")
        st.text_area(
            label="Transcript",
            value=transcript,
            height=350,
            disabled=True,
            label_visibility="collapsed"
        )

        # --- Meeting analysis ---
        with st.spinner("Analyzing meeting..."):
            insights = analyze_meeting(transcript)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Summary")
            st.write(insights.get("summary", ""))

            st.subheader("📋 Decisions")
            decisions = insights.get("decisions", [])
            if decisions:
                for d in decisions:
                    st.markdown(f"- {d}")
            else:
                st.caption("No explicit decisions detected.")

        with col2:
            st.subheader("✅ Action Items")
            action_items_md = pretty_action_items(insights.get("action_items", []))
            if action_items_md:
                st.markdown(action_items_md)
            else:
                st.caption("No action items detected.")

            st.subheader("⚠️ Risks & Open Questions")
            risks = insights.get("risks_open_questions", [])
            if risks:
                for r in risks:
                    st.markdown(f"- {r}")
            else:
                st.caption("No major risks or open questions detected.")

        # --- Export as Markdown ---
        st.download_button(
            "Download summary as Markdown",
            data=build_markdown_export(transcript, insights),
            file_name="meeting_notes.md",
            mime="text/markdown"
        )
