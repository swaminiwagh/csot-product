import { useEffect, useRef, useState } from "react";
import { createWebSocket } from "./websocket.js";
import { useAudioStreamer } from "./useAudioStreamer.js";

function App() {
  const wsRef = useRef(null);
  const audioContextRef = useRef(null);

  const [status, setStatus] = useState("Disconnected");
  const [messages, setMessages] = useState([]);

  // ✅ Create ONE AudioContext for entire app
  useEffect(() => {
    audioContextRef.current = new (window.AudioContext ||
      window.webkitAudioContext)();

    return () => {
      audioContextRef.current?.close();
    };
  }, []);

  // ✅ PCM playback (NO CRACKLING VERSION)
  function playPCMFromBuffer(arrayBuffer) {
  const ctx = audioContextRef.current;
  if (!ctx) return;

  // 🚨 FIX: ensure even byte length
  const buffer = arrayBuffer.slice(0, arrayBuffer.byteLength & ~1);

  const int16 = new Int16Array(buffer);
  const float32 = new Float32Array(int16.length);

  for (let i = 0; i < int16.length; i++) {
    float32[i] = int16[i] / 32768;
  }

  const audioBuffer = ctx.createBuffer(1, float32.length, 24000);
  audioBuffer.copyToChannel(float32, 0);

  const source = ctx.createBufferSource();
  source.buffer = audioBuffer;
  source.connect(ctx.destination);

  // smooth queue
  if (!ctx.nextTime) {
    ctx.nextTime = ctx.currentTime;
  }

  const startTime = ctx.nextTime;
  source.start(startTime);

  ctx.nextTime = startTime + audioBuffer.duration;
}

  useEffect(() => {
  const ws = createWebSocket();

  let isMounted = true;

  ws.onopen = () => {
    if (!isMounted) return;
    console.log("Connected");
    setStatus("Connected");
  };

  ws.onclose = () => {
    if (!isMounted) return;
    console.log("Disconnected");
    setStatus("Disconnected");
  };

  ws.onerror = () => {
    if (!isMounted) return;
    console.log("Error");
    setStatus("Error");
  };

  ws.onmessage = async (event) => {
    if (event.data instanceof Blob) {
  const buffer = await event.data.arrayBuffer();

  // 🔥 ONLY REAL AUDIO
  if (buffer.byteLength < 1000) {
    console.log("Skipping junk audio:", buffer.byteLength);
    return;
  }

  playPCMFromBuffer(buffer);
  return;
}

    try {
      const data = JSON.parse(event.data);

      console.log("📩 Gemini:", data);

      setMessages((prev) => [
        ...prev,
        JSON.stringify(data, null, 2),
      ]);
    } catch {
      console.log("Raw:", event.data);
    }
  };

  wsRef.current = ws;

  return () => {
    isMounted = false;

    console.log("Cleaning WebSocket");

    // IMPORTANT: prevent double-close issue
    if (ws.readyState === 1) {
      ws.close();
    }
  };
}, []);

  const {
    isRecording,
    startRecording,
    stopRecording,
  } = useAudioStreamer(wsRef);

  return (
    <div className="container">
      <h1>🎤 VoicePrep AI</h1>

      <h3>Status: {status}</h3>

      <div className="buttons">
        <button onClick={startRecording}>
          Start Recording
        </button>

        <button onClick={stopRecording}>
          Stop Recording
        </button>
      </div>

      <h2>Recording: {isRecording ? "Yes" : "No"}</h2>

      <div className="chatbox">
        {messages.map((msg, index) => (
          <pre key={index}>{String(msg)}</pre>
        ))}
      </div>
    </div>
  );
}

export default App;