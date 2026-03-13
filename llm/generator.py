import requests

def generate(prompt):

    r = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model":"llama3",
            "messages":[{"role":"user","content":prompt}],
            "stream":False
        }
    )

    return r.json()["message"]["content"]