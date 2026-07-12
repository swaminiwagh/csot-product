import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI, WebSocket
from fastapi import WebSocketDisconnect
import traceback

from app.gemini_client import connect_to_gemini, initialize_gemini
from app.websocket_handler import forward_client_to_gemini, forward_gemini_to_client

app = FastAPI()


@app.websocket("/ws")
async def proxy_endpoint(client_ws: WebSocket):

    await client_ws.accept()
    print("Frontend connected.")

    gemini_ws = None

    try:
        gemini_ws = await connect_to_gemini()
        print("Connected to Gemini.")
        await initialize_gemini(gemini_ws)

        await asyncio.gather(
            forward_client_to_gemini(client_ws, gemini_ws),
            forward_gemini_to_client(client_ws, gemini_ws),
        )

    except WebSocketDisconnect:
        print("Frontend disconnected.")

    except Exception:
        print("========== ERROR ==========")
        traceback.print_exc()
        print("===========================")

    finally:
        # Always cleanly close Gemini connection
        if gemini_ws:
            try:
                await gemini_ws.close()
                print("Gemini connection closed cleanly.")
            except Exception:
                pass


@app.get("/")
def root():
    return {"message": "VoicePrep AI backend running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# from fastapi import FastAPI, WebSocket
# from fastapi import WebSocketDisconnect
# import asyncio
# import traceback
# import asyncio
# import sys

# # Fix for WinError 10053 on Windows with Python 3.12+
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# from app.gemini_client import (
#     connect_to_gemini,
#     initialize_gemini,
# )

# from app.websocket_handler import (
#     forward_client_to_gemini,
#     forward_gemini_to_client,
# )

# app = FastAPI()


# @app.websocket("/ws")
# async def proxy_endpoint(client_ws: WebSocket):

#     await client_ws.accept()
#     print("Frontend connected.")

#     for attempt in range(3):  # retry up to 3 times
#         try:
#             print(f"Connecting to Gemini (attempt {attempt + 1})...")
#             gemini_ws = await connect_to_gemini()
#             print("Connected to Gemini.")
#             await initialize_gemini(gemini_ws)

#             await asyncio.gather(
#                 forward_client_to_gemini(client_ws, gemini_ws),
#                 forward_gemini_to_client(client_ws, gemini_ws),
#             )
#             break  # if we get here cleanly, stop retrying

#         except WebSocketDisconnect:
#             print("Frontend disconnected.")
#             break  # don't retry if frontend left

#         except Exception as e:
#             print(f"========== ERROR (attempt {attempt + 1}) ==========")
#             traceback.print_exc()
#             print("=====================================================")
#             if attempt < 2:
#                 print("Retrying in 2 seconds...")
#                 await asyncio.sleep(2)
#             else:
#                 print("All retries failed.")

# @app.get("/")
# def root():

#     return {
#         "message": "VoicePrep AI backend running"
#     }

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)