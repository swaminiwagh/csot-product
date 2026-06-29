# Week 4 Submission – VoicePrep AI

## GitHub Repository
https://github.com/swaminiwagh/csot (update with your actual repo link)

---

## Project: VoicePrep AI

A voice-native interview coaching agent powered by Gemini Live API. Users can conduct real mock technical and HR interviews entirely through voice — the agent asks questions, listens to answers, gives feedback, and responds naturally to interruptions.

---

## Checklist

### ✅ Custom Persona
Defined in `backend/app/persona.py` as `SYSTEM_PROMPT`.

VoicePrep AI is a warm, professional interview coach with a clear operational boundary (interview prep only), a defined tone (friendly, encouraging, concise), and voice-native instructions (short sentences, no markdown, one question at a time).

Injected via `systemInstruction` in the Gemini setup message in `gemini_client.py`.

---

### ✅ Two Original Custom Tools

Both tools are declared in `gemini_client.py`, implemented in `tools.py`, and dispatched in `dispatcher.py`.

**Tool 1: `get_interview_question(topic)`**
- Takes a topic (Python, DSA, DBMS, OOP, OS)
- Returns a real interview question for that topic from a curated question bank
- Used when the user asks to be quizzed on a specific subject

**Tool 2: `save_interview_score(score, topic)`**
- Writes the interview score and topic to a local JSON file (`interview_scores.json`)
- Persists data across sessions using the filesystem
- Used at the end of an interview session to record performance

Both tools execute real logic and are connected to the live Gemini tool-call dispatch loop in `websocket_handler.py`.

---

### ✅ Barge-in / Interruption Handling

**Backend (`websocket_handler.py`):**
- Detects `serverContent.interrupted: true` in the Gemini message stream
- Immediately sends `{"type": "flush"}` to the frontend
- Does not forward any further audio chunks from that turn

**Frontend (`App.jsx`):**
- `onmessage` handler checks for `data.type === "flush"`
- Resets `audioContextRef.current.nextTime` to `null`, clearing the audio queue
- Prevents stale buffered audio from continuing to play after interruption

---

### ✅ Security
- Gemini API key lives exclusively in `backend/.env`
- Loaded via `python-dotenv` in `config.py`
- No API keys anywhere in frontend source code

---

## Demo Walkthrough

[(video/demo link here)] -- (https://drive.google.com/file/d/1Qws8A8X0MkwBDnC9eS3Hn_vxTlyPFJJ5/view?usp=sharing)

The video demonstrates:
1. Connecting to VoicePrep AI and receiving a voice greeting
2. Requesting an interview — `get_interview_question` fires and the question is spoken aloud
3. Interrupting the agent mid-response — playback stops instantly
4. Completing a session — `save_interview_score` writes the result to `interview_scores.json`