from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from backend.services.chat_service import ask_stream

router = APIRouter()


@router.post("/chat")
def chat(payload: dict):

    question = payload["question"]

    def stream():
        for token in ask_stream(question):
            yield token

    return StreamingResponse(stream(), media_type="text/plain")