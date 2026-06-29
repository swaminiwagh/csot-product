import { useState, useRef, useCallback } from "react";

export function useAudioStreamer(webSocketRef) {
  const [isRecording, setIsRecording] = useState(false);

  const audioContextRef = useRef(null);
  const streamRef = useRef(null);
  const sourceRef = useRef(null);
  const processorRef = useRef(null);

  const initAudio = () => {
    if (!audioContextRef.current) {
      const AudioContext =
        window.AudioContext || window.webkitAudioContext;

      audioContextRef.current = new AudioContext({
        sampleRate: 16000,
      });
    }
  };

  const startRecording = useCallback(async () => {
    console.log("🎤 Start recording clicked");

    initAudio();

    try {
      await audioContextRef.current.resume();

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      streamRef.current = stream;

      const source =
        audioContextRef.current.createMediaStreamSource(stream);

      sourceRef.current = source;

      const processor =
        audioContextRef.current.createScriptProcessor(4096, 1, 1);

      processorRef.current = processor;

      processor.onaudioprocess = (event) => {
        console.log("🎵 Audio chunk captured");

        const input = event.inputBuffer.getChannelData(0);
        const pcm16 = new Int16Array(input.length);

        for (let i = 0; i < input.length; i++) {
          const sample = Math.max(-1, Math.min(1, input[i]));
          pcm16[i] =
            sample < 0
              ? sample * 0x8000
              : sample * 0x7fff;
        }

        const bytes = new Uint8Array(pcm16.buffer);

        let binary = "";
        for (let i = 0; i < bytes.length; i++) {
          binary += String.fromCharCode(bytes[i]);
        }

        const base64 = btoa(binary);

        console.log(
          "WebSocket state:",
          webSocketRef.current?.readyState
        );

        if (
          webSocketRef.current &&
          webSocketRef.current.readyState === WebSocket.OPEN
        ) {
          console.log("📤 Sending audio chunk");

          webSocketRef.current.send(
            JSON.stringify({
              realtimeInput: {
                mediaChunks: [
                  {
                    mimeType: "audio/pcm;rate=16000",
                    data: base64,
                  },
                ],
              },
            })
          );
        } else {
          console.log("❌ WebSocket is not open");
        }
      };

      source.connect(processor);
      processor.connect(audioContextRef.current.destination);

      setIsRecording(true);
    } catch (err) {
      console.error("Recording error:", err);
      alert("Could not access microphone.");
    }
  }, [webSocketRef]);

  const stopRecording = useCallback(() => {
    console.log("🛑 Stopping recording");

    if (processorRef.current) {
      processorRef.current.disconnect();
      processorRef.current = null;
    }

    if (sourceRef.current) {
      sourceRef.current.disconnect();
      sourceRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    // ✅ Tell Gemini that the user has finished speaking
    if (
      webSocketRef.current &&
      webSocketRef.current.readyState === WebSocket.OPEN
    ) {
      console.log("📨 Sending end of turn");

      webSocketRef.current.send(
        JSON.stringify({
          realtimeInput: {
            audioStreamEnd: true,
          },
        })
      );
    }

    setIsRecording(false);
  }, [webSocketRef]);

  return {
    isRecording,
    startRecording,
    stopRecording,
  };
}