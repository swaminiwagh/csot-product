import json
import websockets

from app.config import GEMINI_WS_URL, MODEL
from app.persona import SYSTEM_PROMPT


async def connect_to_gemini():
    return await websockets.connect(
        GEMINI_WS_URL,
        ping_interval=20,
        ping_timeout=60,
        close_timeout=10,
    )


def get_setup_message():
    return {
        "setup": {
            "model": MODEL,
            "generationConfig": {
                "responseModalities": ["AUDIO"]
            },
            "systemInstruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
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
                        },
                        {
                            "name": "get_interview_question",
                            "description": "Returns an interview question for a given topic.",
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "topic": {
                                        "type": "STRING",
                                        "description": "Interview topic such as Python, DSA, DBMS, OOP or OS."
                                    }
                                },
                                "required": ["topic"]
                            }
                        },
                        {
                            "name": "save_interview_score",
                            "description": "Stores the interview score for a completed interview.",
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "score": {
                                        "type": "NUMBER",
                                        "description": "Interview score."
                                    },
                                    "topic": {
                                        "type": "STRING",
                                        "description": "Interview topic."
                                    }
                                },
                                "required": ["score", "topic"]
                            }
                        }
                    ]
                }
            ]
        }
    }


async def initialize_gemini(gemini_ws):
    setup_message = get_setup_message()
    await gemini_ws.send(json.dumps(setup_message))