import asyncio

async def forward_client_to_gemini(client_ws, gemini_ws):
    while True:
        data = await client_ws.receive_text()
        await gemini_ws.send(data)


async def forward_gemini_to_client(client_ws, gemini_ws):
    while True:
        message = await gemini_ws.recv()

        if isinstance(message, str):
            await client_ws.send_text(message)
        else:
            await client_ws.send_bytes(message)