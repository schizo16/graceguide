"""Chat API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from chat.service import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    language: str = "en"


class ChatResponse(BaseModel):
    response: str
    is_streaming: bool = False


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = generate_response(request.message, request.language)
    return ChatResponse(response=response)
