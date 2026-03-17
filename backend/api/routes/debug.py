from fastapi import APIRouter
from backend.services.chat_service import build_context

router = APIRouter()

@router.post("/debug")
def debug_query(query: str):

    from backend.observability.trace import RAGTrace

    trace = RAGTrace(query)

    context = build_context(query, trace)

    return {
        "query": query,
        "trace": trace.data,
        "context": context
    }