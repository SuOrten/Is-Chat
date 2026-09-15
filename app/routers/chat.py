# app/routers/chat.py

import httpx
from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.model_garden_service import ModelGardenService

router = APIRouter(prefix="/api/v1", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Kullanıcı mesajını alır, Qwen'den cevap üretir."""
    service = ModelGardenService()
    try:
        reply = await service.generate_response(request.message)
    except httpx.HTTPStatusError as e:
        # Model Garden tarafı hata döndürdüyse (örn. 401, 429)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Model servisi hata döndü: {e.response.status_code}",
        )
    except Exception:
        # Beklenmeyen hatalar
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model çağrısı sırasında beklenmeyen bir hata oluştu.",
        )

    return ChatResponse(reply=reply, model=service.model)