from fastapi import APIRouter
from backend.services.chat_service import ask

router = APIRouter()

@router.post("/chat")
def chat_endpoint(payload: dict):

    question = payload["question"]

    answer = ask(question)

    return {"answer": answer}