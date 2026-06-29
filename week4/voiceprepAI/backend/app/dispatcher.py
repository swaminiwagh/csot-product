# app/dispatcher.py

from app.tools import (
    get_current_time,
    get_interview_question,
    save_interview_score,
)

TOOLS = {
    "get_current_time": get_current_time,
    "get_interview_question": get_interview_question,
    "save_interview_score": save_interview_score,
}


def dispatch(tool_name, arguments):
    """
    Execute the requested tool.
    """

    if tool_name not in TOOLS:
        return {
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        return TOOLS[tool_name](**arguments)

    except Exception as e:
        return {
            "error": str(e)
        }