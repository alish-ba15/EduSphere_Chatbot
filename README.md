# EduSphere Chatbot

EduSphere is a Streamlit educational assistant with two role-based experiences: students can ask questions about lecture transcripts, and teachers can generate multiple-choice quizzes from PDF or text documents. The project uses Google Gemini through LangChain, with Chroma for transcript retrieval and Deepgram for optional audio transcription/indexing.

## Features

- Student Q&A over indexed lecture transcripts
- Teacher quiz generation from PDF or text uploads
- Quiz export to a Word document
- Optional audio transcription and Chroma indexing through `indexing.py`

## Repository structure

- `app.py` — Streamlit entry point and role selector
- `menu.py` — role-based navigation
- `pages/chat_bot.py` — lecture transcript Q&A
- `pages/quiz.py` — quiz creation and Word export
- `pages/pdf_load.py`, `pages/pdf_design.py`, `pages/json_to_word.py` — document and quiz helpers
- `indexing.py` — transcribes audio and indexes transcripts
- `Output.json` — lecture transcript data used by the chatbot
- `YouTube_Audio/` — optional source audio for transcription
- `Chroma_Indexing_db/` — local vector index created by the indexing workflow

## Requirements

Use Python 3.10 or newer. The project needs Google AI credentials for chatbot and quiz generation. Audio indexing additionally requires Deepgram credentials.

Create and activate a virtual environment from the repository root:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
```

Install dependencies and configure credentials in your shell or a local `.env` file:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

```dotenv
GOOGLE_API_KEY=your-google-ai-key
DEEPGRAM_API_KEY=your-deepgram-key
```

Never commit real API keys. `DEEPGRAM_API_KEY` is only needed for audio transcription/indexing.

## Run the Streamlit app

From the repository root:

```bash
streamlit run app.py
```

Choose a role on the landing page. Students can open the lecture chat; teachers can open quiz generation and upload a PDF or TXT file.

## Build the lecture index (optional)

Place authorized MP3 or WAV lecture audio files in `YouTube_Audio/`, set `DEEPGRAM_API_KEY` and `GOOGLE_API_KEY`, then run:

```bash
python indexing.py
```

This writes transcript data to `Output.json` and creates a local `Chroma_Indexing_db/` vector index. The chatbot expects both the transcript JSON and a compatible indexed Chroma collection. Do not index or share copyrighted or private recordings unless you have permission.

## Notes and limitations

- Selectable roles are navigation choices, not authentication or access control.
- Model responses and generated quizzes can be inaccurate; educators should review quiz questions and answers before using them.
- The chatbot is intended to answer from the indexed lecture content, but retrieval and generated responses may still omit or misstate information.
- This project is an educational demo, not a production learning-management system.
