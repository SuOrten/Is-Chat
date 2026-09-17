# app/routers/chat.py

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.model_garden_service import ModelGardenService

router = APIRouter(prefix="/api/v1", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    """
    Korumalı chat: önce login olup token al, sonra konuş.

    Token'sız istek 401 döner. Kullanıcı adı system prompt'a eklenir.
    """
    service = ModelGardenService()
    try:
        reply = await service.generate_response(
            request.message,
            user_name=current_user.username,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Model servisi hata döndü: {e.response.status_code}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model çağrısı sırasında beklenmeyen bir hata oluştu.",
        )

    return ChatResponse(reply=reply, model=service.model)