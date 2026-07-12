# Week 5 Submission – VoicePrep AI

## GitHub Repository
https://github.com/swaminiwagh/csot-product

## Demo Video
(add your screen recording link here)

---

## Project Summary

VoicePrep AI is a voice-native mock interview coaching agent built with Gemini Live API, FastAPI, and React. Users conduct full mock technical and HR interviews entirely through voice — no typing required.

---

## Week 5 Deliverables

### ✅ Working Prototype
- Backend: FastAPI WebSocket proxy connecting frontend to Gemini Live API
- Frontend: React + Vite app with real-time PCM audio capture and playback
- Voice-native persona with operational boundary (interview prep only)
- Two custom tools with real logic (no hardcoded dummy returns)
- Barge-in handling: interruption detected via Gemini VAD, frontend audio queue flushed instantly

### ✅ Evaluation Log
See `EVALUATION_LOG.md` — documents 3 edge cases tested with results and average response latency.

---

## Architecture

User Mic → React Frontend (Vercel)
→ FastAPI Backend (Railway)
→ Gemini Live API (WebSocket)
→ Audio response back to user

---

## Custom Tools

**Tool 1: get_interview_question(topic)**
- Accepts topic: Python, DSA, DBMS, OOP, OS
- Returns a real interview question from a curated bank
- Triggered when user asks to be quizzed on a subject

**Tool 2: save_interview_score(score, topic)**
- Writes score + topic + timestamp to interview_scores.json
- Persists data using the filesystem
- Triggered at end of interview session

---

## Security
- GEMINI_API_KEY stored only in backend .env
- Loaded via python-dotenv in config.py
- Zero API keys in any frontend file

---
