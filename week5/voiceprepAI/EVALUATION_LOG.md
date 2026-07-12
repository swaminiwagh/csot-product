# VoicePrep AI – Evaluation Log

## App: VoicePrep AI
## Model: gemini-2.5-flash-native-audio-preview-12-2025
## Test Date: June 2026

---

## Average Response Latency
Approximately 1–2 seconds between finishing a spoken question and receiving the first audio response from Gemini.

---

## Edge Case Tests

### Test 1: Long Silence (Mumble/No Input)
**What I did:** Started recording and stayed completely silent for 5+ seconds, then stopped.

**Expected:** App should not crash. Gemini should either wait or respond with a prompt.

**What happened:** The WebSocket stayed connected. When recording was stopped, Gemini received the end-of-turn signal and responded with a gentle prompt asking if I was still there.

**Result:** ✅ Handled gracefully — no crash, no broken state.

---

### Test 2: Out-of-Scope Question (Guardrail Test)
**What I did:** Asked VoicePrep AI "What is the recipe for pasta?"

**Expected:** Agent should redirect back to interview prep without breaking character.

**What happened:** VoicePrep AI politely said it could only help with interview preparation and offered to start a mock interview instead.

**Result:** ✅ Persona boundary held — redirected cleanly.

---

### Test 3: Barge-in Mid-Response (Interruption Test)
**What I did:** Asked for an interview question, then interrupted the AI mid-response by asking a different question.

**Expected:** Audio playback should stop instantly and the agent should immediately switch to answering the new question

**What happened:** Gemini's VAD successfully detected the interruption and captured the new question. However, instead of stopping its current response, the agent first completed the ongoing answer. After a brief pause, it then responded to the interrupted question. The interruption was recognized correctly, but the response was queued rather than handled immediately.

**Result:** ⚠️ Partially working — interruption is detected and the new question is answered correctly, but the agent does not stop its ongoing response immediately. Instead, it finishes the current response before switching to the interrupted query.

---

## Notes
- App runs fully on Gemini free tier — no billing required
- API key is secured in backend `.env` only — never exposed to frontend
- Two edge cases passed without crashes/errors and One edge case passed partially