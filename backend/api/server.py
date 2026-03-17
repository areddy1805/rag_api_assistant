from fastapi import FastAPI
from backend.api.routes.chat import router as chat_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(debug.router)