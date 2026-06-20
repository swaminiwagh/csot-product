import json

setup_message = {
    "setup": {
        "model": "models/gemini-2.5-flash-native-audio-preview-12-2025",
        "generationConfig": {
            "responseModalities": ["AUDIO"]
        },
        "systemInstruction": {
            "parts": [
                {
                    "text": "You are a helpful smart echo box."
                }
            ]
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
                    }
                ]
            }
        ]
    }
}

if __name__ == "__main__":
    print(json.dumps(setup_message, indent=2))