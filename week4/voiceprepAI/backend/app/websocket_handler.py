# app/websocket_handler.py

import json

from app.dispatcher import dispatch


async def forward_client_to_gemini(client_ws, gemini_ws):
    """
    Receives messages from the frontend and forwards them to Gemini.
    """

    while True:
        data = await client_ws.receive_text()

        print("➡️ Received from frontend")
        print("➡️ Sending to Gemini")

        await gemini_ws.send(data)


async def forward_gemini_to_client(client_ws, gemini_ws):
    """
    Receives Gemini responses.

    Handles:
    - Audio
    - Tool calls
    - Interruptions
    - Turn completion
    """

    while True:

        message = await gemini_ws.recv()

        # -----------------------------------
        # Gemini sometimes sends JSON as bytes.
        # Try decoding before assuming audio.
        # -----------------------------------
        if isinstance(message, bytes):

            try:
                decoded = message.decode("utf-8")
                message = decoded

            except UnicodeDecodeError:

                print("🔊 Binary audio received")

                await client_ws.send_bytes(message)

                continue

        print("⬅️ RAW Gemini message:", message)

        # -----------------------------------
        # Parse JSON
        # -----------------------------------
        try:
            data = json.loads(message)

        except Exception:

            print("⚠️ Non JSON response")

            await client_ws.send_text(message)

            continue

        # -----------------------------------
        # Setup Complete
        # -----------------------------------
        if "setupComplete" in data:

            print("✅ Gemini setup complete")

            continue

        # -----------------------------------
        # Barge-in
        # -----------------------------------
        if (
            "serverContent" in data
            and data["serverContent"].get("interrupted")
        ):

            print("🛑 User interrupted Gemini")

            await client_ws.send_text(
                json.dumps(
                    {
                        "type": "flush"
                    }
                )
            )

            continue

        # -----------------------------------
        # Turn Complete
        # -----------------------------------
        if (
            "serverContent" in data
            and data["serverContent"].get("turnComplete")
        ):

            print("✅ Gemini finished speaking")

        # -----------------------------------
        # Tool Calls
        # -----------------------------------
        if "toolCall" in data:

            print("🛠 Tool call received")

            responses = []

            for fn in data["toolCall"].get("functionCalls", []):

                tool_name = fn["name"]
                arguments = fn.get("args", {})

                print(f"Calling tool: {tool_name}")

                result = dispatch(
                    tool_name,
                    arguments,
                )

                responses.append(
                    {
                        "id": fn["id"],
                        "name": tool_name,
                        "response": result,
                    }
                )

            tool_response = {
                "toolResponse": {
                    "functionResponses": responses
                }
            }

            print("➡️ Sending tool response to Gemini")

            await gemini_ws.send(
                json.dumps(tool_response)
            )

            continue

        # -----------------------------------
        # Forward everything else
        # -----------------------------------
        print("➡️ Forwarding Gemini response to frontend")

        await client_ws.send_text(
            json.dumps(data)
        )