import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:instruct"


def chat(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )

    return response.json()["message"]["content"]