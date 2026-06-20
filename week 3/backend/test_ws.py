import asyncio
import websockets

async def test_websocket():
    uri = "wss://echo.websocket.events"
    print(f"Connecting to {uri}...")

    async with websockets.connect(uri) as websocket:
        print("Connection open!")

        # Send 3 messages over the SAME connection
        for i in range(1, 4):
            await websocket.send(f"Hello, WebSocket! (message {i})")
            response = await websocket.recv()
            print(f"Server replied: {response}")
            await asyncio.sleep(2)

        print("One connection handled 3 round-trips.")

if __name__ == "__main__":
    asyncio.run(test_websocket())