# app/utils.py

import base64
import json


def encode_bytes(data: bytes) -> str:
    """
    Convert bytes into base64 string.
    """
    return base64.b64encode(data).decode("utf-8")


def decode_base64(data: str) -> bytes:
    """
    Decode base64 string back into bytes.
    """
    return base64.b64decode(data)


def safe_json_loads(message):
    """
    Safely parse JSON.

    Returns:
        dict or None
    """

    try:
        return json.loads(message)

    except Exception:
        return None


def build_tool_response(function_responses):
    """
    Create Gemini tool response payload.
    """

    return {
        "toolResponse": {
            "functionResponses": function_responses
        }
    }