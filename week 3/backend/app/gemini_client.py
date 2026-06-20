import websockets
from app.config import GEMINI_WS_URL

async def connect_to_gemini():
    """
    Opens a WebSocket connection to Gemini Live API.
    """
    websocket = await websockets.connect(GEMINI_WS_URL)
    return websocket