import io
import os
from typing import Dict, Any, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # <-- make sure this is here

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------- Helper to build markdown export ---------
def build_markdown_export(transcript: str, insights: dict) -> str:
    """
    Build a markdown export of the meeting notes.
    """
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


# ---------- 1. Transcription ----------

def transcribe_audio(file_bytes: bytes, filename: str) -> str:
    """
    Takes raw audio bytes and filename, returns transcript text.
    """
    # OpenAI Python client expects a file-like object
    audio_file = io.BytesIO(file_bytes)
    audio_file.name = filename  # important for some clients

    transcript = client.audio.transcriptions.create(
        model="whisper-1",  # or "whisper-1" depending on your access
        file=audio_file,
        response_format="text"
    )
    # If response_format="text", transcript is a plain string
    return transcript


# ---------- 2. LLM meeting analysis ----------

SYSTEM_PROMPT = """
You are a Meeting Whisperer assistant.

You take a verbatim meeting transcript and produce:
1) a concise summary,
2) a list of decisions,
3) a list of action items with owners and due dates (if mentioned),
4) key risks or open questions.

Return your answer as JSON with this exact structure:

{
  "summary": "short paragraph",
  "decisions": ["..."],
  "action_items": [
    {
      "owner": "Name or 'Unassigned'",
      "task": "what needs to be done",
      "due": "date or 'N/A'"
    }
  ],
  "risks_open_questions": ["..."]
}
"""

def analyze_meeting(transcript: str) -> Dict[str, Any]:
    """
    Use an LLM to turn a raw transcript into structured meeting insights.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    import json
    return json.loads(content)


def pretty_action_items(ai: List[Dict[str, Any]]) -> str:
    """
    Turn action items into a markdown list string.
    """
    lines = []
    for item in ai:
        owner = item.get("owner", "Unassigned")
        task = item.get("task", "").strip()
        due = item.get("due", "N/A")
        if not task:
            continue
        lines.append(f"- **{owner}** → {task} _(Due: {due})_")
    return "\n".join(lines)

def build_markdown_export(transcript: str, insights: str) -> str:
    return f"""# Meeting Notes

## 📝 Insights
{insights}

---

## 🎙 Transcript
{transcript}
"""

