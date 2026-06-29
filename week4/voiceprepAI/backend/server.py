from fastapi import FastAPI, WebSocket
from fastapi import WebSocketDisconnect
import asyncio
import traceback

from app.gemini_client import (
    connect_to_gemini,
    initialize_gemini,
)

from app.websocket_handler import (
    forward_client_to_gemini,
    forward_gemini_to_client,
)

app = FastAPI()


@app.websocket("/ws")
async def proxy_endpoint(client_ws: WebSocket):

    await client_ws.accept()

    print("Frontend connected.")

    try:

        gemini_ws = await connect_to_gemini()

        print("Connected to Gemini.")

        await initialize_gemini(gemini_ws)

        await asyncio.gather(

            forward_client_to_gemini(
                client_ws,
                gemini_ws,
            ),

            forward_gemini_to_client(
                client_ws,
                gemini_ws,
            ),

        )

    except WebSocketDisconnect:

        print("Frontend disconnected.")

    except Exception:

        print("========== ERROR ==========")

        traceback.print_exc()

        print("===========================")


@app.get("/")
def root():

    return {
        "message": "VoicePrep AI backend running"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)