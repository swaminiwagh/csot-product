import os
import json
import asyncio

import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import uvicorn
import traceback
from datetime import datetime

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"

GEMINI_WS_URL = (
    "wss://generativelanguage.googleapis.com/ws/"
    "google.ai.generativelanguage.v1beta.GenerativeService."
    f"BidiGenerateContent?key={GEMINI_API_KEY}"
)

app = FastAPI()


async def forward_client_to_gemini(client_ws, gemini_ws):
    while True:
        data = await client_ws.receive_text()
        print("➡️ Received from frontend")
        print("➡️ Sending to Gemini")
        await gemini_ws.send(data)


async def forward_gemini_to_client(client_ws, gemini_ws):
    while True:
        message = await gemini_ws.recv()

        print("⬅️ RAW Gemini message:", message)

        if isinstance(message, bytes):
            print("⬅️ Gemini sent binary audio")
            await client_ws.send_bytes(message)
            continue

        try:
            data = json.loads(message)
        except Exception:
            print("⬅️ Non-JSON message from Gemini")
            await client_ws.send_text(message)
            continue

        # Handle tool calls
        if "toolCall" in data:
            print("🛠️ Tool call received!")

            responses = []

            for fn in data["toolCall"].get("functionCalls", []):
                if fn["name"] == "get_current_time":
                    current_time = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    print("🕒 Current time:", current_time)

                    responses.append({
                        "id": fn["id"],
                        "name": "get_current_time",
                        "response": {
                            "current_time": current_time
                        }
                    })

            tool_response = {
                "toolResponse": {
                    "functionResponses": responses
                }
            }

            print("➡️ Sending tool response to Gemini")
            await gemini_ws.send(json.dumps(tool_response))
            continue

        print("➡️ Forwarding Gemini response to frontend")
        await client_ws.send_text(json.dumps(data))


@app.websocket("/ws")
async def proxy_endpoint(client_ws: WebSocket):
    await client_ws.accept()
    print("Frontend connected.")

    try:
        async with websockets.connect(GEMINI_WS_URL) as gemini_ws:
            print("Connected to Gemini.")

            setup_message = {
                "setup": {
                    "model": MODEL,
                    "generationConfig": {
                        "responseModalities": ["AUDIO"]
                    },
                    "systemInstruction": {
                        "parts": [
                            {
                                "text": "You are VoicePrep AI, a helpful interview coach."
                            }
                        ]
                    },
                    "tools": [
                        {
                            "functionDeclarations": [
                                {
                                    "name": "get_current_time",
                                    "description": "Returns the current local time.",
                                    "parameters": {
                                        "type": "OBJECT",
                                        "properties": {},
                                        "required": []
                                    }
                                }
                            ]
                        }
                    ]
                }
            }

            await gemini_ws.send(json.dumps(setup_message))

            await asyncio.gather(
                forward_client_to_gemini(client_ws, gemini_ws),
                forward_gemini_to_client(client_ws, gemini_ws),
            )

    except WebSocketDisconnect:
        print("Frontend disconnected.")

    except Exception as e:
        print("========== BACKEND ERROR ==========")
        traceback.print_exc()
        print("===================================")


@app.get("/")
def root():
    return {"message": "VoicePrep AI backend running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)