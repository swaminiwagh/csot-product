import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"

GEMINI_WS_URL = (
    "wss://generativelanguage.googleapis.com/ws/"
    "google.ai.generativelanguage.v1beta.GenerativeService."
    f"BidiGenerateContent?key={GEMINI_API_KEY}"
)
print("API Key loaded:", GEMINI_API_KEY is not None)
print("First 10 chars:", GEMINI_API_KEY[:10] if GEMINI_API_KEY else "None")