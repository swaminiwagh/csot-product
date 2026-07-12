# 🎤 VoicePrep AI

A voice-native mock interview coach built with Gemini Live API, FastAPI, and React. Have a full interview conversation entirely by voice — the AI asks questions, listens, adapts, and can be interrupted naturally mid-sentence.

---

## What It Does

- Conducts mock technical and HR interviews over voice in real time
- Fetches interview questions by topic (Python, DSA, DBMS, OOP, OS)
- Saves your interview score locally at the end of a session
- Handles barge-in: interrupt the agent mid-response and it stops
- Runs fully on Gemini API free tier — no billing required

---

## Project Structure

voiceprepAI/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── dispatcher.py
│   │   ├── gemini_client.py
│   │   ├── persona.py
│   │   ├── tools.py
│   │   ├── utils.py
│   │   └── websocket_handler.py
│   ├── server.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   └── src/
│       ├── App.css
│       ├── App.jsx
│       ├── index.css
│       ├── main.jsx
│       ├── useAudioStreamer.js
│       └── websocket.js
├── .gitignore
├── EVALUATION_LOG.md
├── README.md
└── SUBMISSION.md

---

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Gemini API key (free tier, from https://aistudio.google.com)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` inside `backend/`:

GEMINI_API_KEY=your_key_here

Start server:
```bash
uvicorn server:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

---

## How to Use

1. Open the app — status shows Connected
2. Click Start Session and speak to VoicePrep AI
3. Ask for an interview: "Can you give me a Python interview question?"
4. Answer out loud
5. Speak over the agent at any point to interrupt
6. Click End Session when done

---

## Tools

| Tool | What It Does |
|---|---|
| `get_interview_question` | Returns a mock interview question for Python / DSA / DBMS / OOP / OS |
| `save_interview_score` | Writes score + topic + timestamp to `interview_scores.json` |

---

## Tech Stack

- Gemini Live API — gemini-2.5-flash-native-audio-preview-12-2025
- FastAPI + websockets — Python proxy backend
- React + Vite — Frontend
- Web Audio API — PCM audio playback
- python-dotenv — Secure API key management