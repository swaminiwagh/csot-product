from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Middleman is running!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Frontend client connected!")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from frontend: {data}")
            await websocket.send_text(f"Proxy echo: {data}")
    except WebSocketDisconnect:
        print("Frontend client disconnected.")

if __name__ == "__main__":
    print("Starting proxy server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)