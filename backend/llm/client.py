import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"

REWRITE_MODEL = "qwen2.5:3b"
ANSWER_MODEL = "qwen2.5:7b"


def chat(prompt, model):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "num_predict": 200
            }
        }
    )

    data = response.json()

    return data["message"]["content"]


def chat_stream(prompt, model):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "options": {
                "num_predict": 200
            }
        },
        stream=True
    )

    for line in response.iter_lines():

        if not line:
            continue

        data = json.loads(line.decode("utf-8"))

        if "message" in data and "content" in data["message"]:
            yield data["message"]["content"]