# 🎤 VoicePrep AI

A voice-native mock interview coach built with Gemini Live API, FastAPI, and React. Have a full interview conversation — entirely by voice — with an AI that asks questions, listens, adapts, and can be interrupted naturally mid-sentence.

---

## What It Does

- Conducts mock technical and HR interviews over voice in real time
- Fetches interview questions by topic (Python, DSA, DBMS, OOP, OS)
- Saves your interview score locally at the end of a session
- Handles barge-in: interrupt the agent mid-response and it stops instantly
- Runs fully on the Gemini API free tier — no billing required

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

│   └── .env

│

├── frontend/

│   └── src/

│       ├── App.jsx

│       ├── useAudioStreamer.js

│       ├── websocket.js

│       ├── App.css

│       └── index.css

│

└── barge_in.py

---

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Gemini API key (free tier, from https://aistudio.google.com)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`: GEMINI_API_KEY=your_key_here

Start the server:

```bash
uvicorn server:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## How to Use

1. Open the app — status shows **Connected**
2. Click **Start Recording** and speak to VoicePrep AI
3. Ask for an interview: *"Can you give me a Python interview question?"*
4. Answer the question out loud
5. Interrupt the agent at any point by speaking over it — playback stops immediately
6. Click **Stop Recording** when done

---

## Tools

| Tool | Trigger | What It Does |
|---|---|---|
| `get_interview_question` | User asks for a question on a topic | Returns a mock interview question for Python / DSA / DBMS / OOP / OS |
| `save_interview_score` | End of interview session | Writes score + topic + timestamp to `interview_scores.json` |

---

## Key Implementation Details

**Barge-in:** Gemini sends `serverContent.interrupted: true` when the user speaks over the model. The backend catches this in `websocket_handler.py` and immediately sends `{"type": "flush"}` to the frontend. The frontend resets `audioContextRef.current.nextTime` to stop queued audio from playing.

**Audio Pipeline:** Mic audio is captured at 16kHz, encoded to PCM16, base64-encoded, and sent as `realtimeInput.mediaChunks`. Gemini returns audio as base64 `inlineData` inside `serverContent.modelTurn.parts`, decoded and played via Web Audio API at 24kHz.

**Tool Dispatch:** Gemini sends `toolCall.functionCalls` over the WebSocket. `dispatcher.py` maps tool names to Python functions, executes them, and returns `toolResponse.functionResponses` back to Gemini within the same session.

---

## Tech Stack

- **Gemini Live API** — `gemini-2.5-flash-native-audio-preview-12-2025`
- **FastAPI + websockets** — Python proxy backend
- **React + Vite** — Frontend
- **Web Audio API** — PCM audio playback
- **python-dotenv** — Secure API key management

