# VoicePrep AI — Submission Report

## 1. Data Flow Architecture

VoicePrep AI implements a real-time bidirectional audio pipeline for conversational interview practice. The system is divided into three components: frontend (React), backend (FastAPI WebSocket server), and Gemini Live Audio API.

On the frontend, microphone input is captured using the Web Audio API (`getUserMedia`) and processed through a `ScriptProcessorNode`. The raw audio is converted into PCM Float32 chunks and throttled at 100ms intervals to prevent network congestion. These chunks are streamed over a persistent WebSocket connection to the backend.

The backend acts as an intermediary streaming layer. It receives raw audio chunks from the frontend, forwards them to the Gemini Live API WebSocket, and receives both text and audio responses. The backend then relays these responses back to the frontend in real time.

On the frontend, incoming audio is decoded from Int16 PCM format into Float32 and played using the `AudioBufferSourceNode` with scheduled playback to ensure smooth, gap-free audio output.

---

## 2. Dual WebSocket Connection Handling

The system uses two simultaneous WebSocket connections:

1. **Frontend ↔ Backend WebSocket**
   - Handles streaming microphone audio input
   - Sends `Float32 PCM chunks` continuously
   - Receives processed AI responses (text + audio)

2. **Backend ↔ Gemini WebSocket**
   - Maintains persistent connection with Gemini Live API
   - Streams audio input to the model
   - Receives real-time audio + text responses

The backend acts as a bridge between these two WebSockets, ensuring format compatibility and maintaining synchronization between user input and model output.

A key design challenge was preventing feedback loops and ensuring that only user audio is forwarded to Gemini, while AI responses are strictly sent back to the frontend without reprocessing.

---

## 3. Challenges Faced

### 3.1 Audio Overload and Latency
Initially, the system flooded the backend with high-frequency audio packets, causing latency spikes and unstable responses. This was resolved by introducing a **100ms throttling mechanism** in the audio capture loop.

---

### 3.2 PCM Audio Distortion
Audio playback suffered from crackling and distortion due to misaligned PCM buffer sizes. This was fixed by properly converting Int16 PCM data into normalized Float32 format and ensuring consistent buffer sizing before playback.

---

### 3.3 WebSocket Instability
Frequent disconnects occurred during rapid audio streaming. This was resolved by improving WebSocket lifecycle management, ensuring proper cleanup on component unmount and controlled stream termination using an explicit `audioStreamEnd` signal.

---

### 3.4 Audio Synchronization
Incoming audio chunks from Gemini arrived in variable sizes, causing playback jitter. This was solved using scheduled playback via `AudioContext.nextTime`, ensuring sequential and smooth audio rendering.

---

## 4. Conclusion

VoicePrep AI successfully demonstrates a low-latency, real-time voice-based AI interview system using dual WebSocket architecture and streaming audio pipelines. Despite challenges in audio synchronization and network stability, the system achieves smooth bidirectional voice interaction with minimal delay and high responsiveness.