import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Gemini REST endpoint
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

headers = {
    "x-goog-api-key": api_key
}

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain the difference between a REST API and a WebSocket in one sentence."
                }
            ]
        }
    ]
}

print("Sending request to Gemini...")

response = requests.post(url, headers=headers, json=payload)

if response.status_code != 200:
    print("Error:", response.status_code)
    print(response.text)
    raise SystemExit(1)

answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]

print("\nGemini Response:\n")
print(answer)