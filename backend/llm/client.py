import requests
import json
import time

from backend.observability.logger import logger
from backend.observability.trace import RAGTrace

OLLAMA_URL = "http://localhost:11434/api/chat"

REWRITE_MODEL = "qwen2.5:3b"
ANSWER_MODEL = "qwen2.5:7b"


def chat(prompt, model):

    start = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "num_predict": 120
            }
        }
    )

    data = response.json()

    latency = time.time() - start

    prompt_tokens = data.get("prompt_eval_count", 0)
    completion_tokens = data.get("eval_count", 0)

    total_tokens = prompt_tokens + completion_tokens

    logger.info(
        f"[LLM] model={model} "
        f"prompt_tokens={prompt_tokens} "
        f"completion_tokens={completion_tokens} "
        f"total_tokens={total_tokens} "
        f"latency={latency:.2f}s"
    )

    trace = RAGTrace.current
    if trace:
        trace.add_tokens(prompt_tokens, completion_tokens)

    return data["message"]["content"]


def chat_stream(prompt, model):

    start = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "options": {
                "num_predict": 120
            }
        },
        stream=True
    )

    prompt_tokens = 0
    completion_tokens = 0

    for line in response.iter_lines():

        if not line:
            continue

        data = json.loads(line.decode("utf-8"))

        if "prompt_eval_count" in data:
            prompt_tokens = data["prompt_eval_count"]

        if "eval_count" in data:
            completion_tokens = data["eval_count"]

        if "message" in data and "content" in data["message"]:
            yield data["message"]["content"]

    latency = time.time() - start

    total_tokens = prompt_tokens + completion_tokens

    logger.info(
        f"[LLM_STREAM] model={model} "
        f"prompt_tokens={prompt_tokens} "
        f"completion_tokens={completion_tokens} "
        f"total_tokens={total_tokens} "
        f"latency={latency:.2f}s"
    )

    trace = RAGTrace.current
    if trace:
        trace.add_tokens(prompt_tokens, completion_tokens)