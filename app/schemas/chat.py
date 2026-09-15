# app/schemas/chat.py

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Kullanıcının gönderdiği mesaj."""
    message: str = Field(..., min_length=1, max_length=2000, description="Kullanıcı mesajı")


class ChatResponse(BaseModel):
    """Modelin ürettiği cevap."""
    reply: str
    model: str