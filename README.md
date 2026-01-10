🦉 Meeting Whisperer

Turn messy meetings into clear summaries, decisions, and action items.

Meeting Whisperer is a lightweight app that listens to your meetings (via uploaded audio), transcribes them, and automatically generates structured notes — including summaries, decisions, action items, and open questions.

Built with:

🎧 Whisper-style speech-to-text (OpenAI)

🤖 LLM-powered analysis

🖥️ Streamlit UI

✨ Features

✔ Upload meeting recordings (mp3, wav, m4a, etc.)
✔ High-quality transcription
✔ Automatic meeting summary
✔ Extracted decisions
✔ Action items with owners & due dates
✔ Risks & open questions
✔ Export notes as Markdown

Privacy-first: nothing is stored unless you choose to save or export.

🛠️ Tech Stack

Python

Streamlit — simple UI

OpenAI API — transcription + reasoning

dotenv — environment config

pydub / ffmpeg — audio support

📦 Project Structure
meeting-whisperer/
├─ app.py
├─ meeting_core.py
├─ requirements.txt
├─ .env
└─ README.md

🚀 Getting Started
1️⃣ Clone the repo
git clone https://github.com/your-username/meeting-whisperer.git
cd meeting-whisperer

2️⃣ Install dependencies
pip install -r requirements.txt


You may also need ffmpeg installed (system-level).

Mac (brew):

brew install ffmpeg


Ubuntu:

sudo apt install ffmpeg


Windows:

Download from: https://ffmpeg.org/download.html

Add it to PATH.

3️⃣ Add your API key

Create a file called .env in the project root:

OPENAI_API_KEY=your_key_here

4️⃣ Run the app
streamlit run app.py


Open your browser at:

http://localhost:8501


Upload an audio file — and you’re done 🎉

🧠 How It Works

1️⃣ You upload audio
2️⃣ Whisper model transcribes speech → text
3️⃣ LLM analyzes the transcript and produces:

summary

decisions

action items

risks / questions

4️⃣ You can view or download the results.

🔒 Privacy & Ethics

You should only upload recordings you are legally allowed to use.

Always inform meeting participants when recording.

Avoid storing sensitive transcripts unless necessary.

🗺️ Roadmap

Planned improvements:

🎤 live microphone recording

👥 speaker identification

🗂️ meeting history & tagging

📧 auto-generate follow-up email

🔍 search across meetings

🌐 optional cloud storage

🤝 Contributing

Pull requests and ideas welcome!

Fork repo

Create feature branch

Submit PR

🧾 License

MIT — free to use, modify, and build on.