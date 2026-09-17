# app/routers/greetings.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import GreetingRequest, GreetingResponse, UserResponse
from app.services.greeting_service import GreetingService

router = APIRouter(prefix="/api/v1", tags=["Greetings"])


@router.post("/greetings", response_model=GreetingResponse)
async def create_greeting(request: GreetingRequest, db: Session = Depends(get_db)):
    service = GreetingService(db)

    try:
        return service.create_greeting(request.username)
    except ValueError as e:
        error_msg = str(e)
        if "yasaklı" in error_msg.lower():
            # Yasaklı kullanıcı -> 403 Forbidden
            raise HTTPException(status_code=403, detail=error_msg)
        else:
            # Kullanıcı bulunamadı -> 404 Not Found
            raise HTTPException(status_code=404, detail=error_msg)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """ID ile kullanıcı bul."""
    service = GreetingService(db)
    user = service.user_repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    return UserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        age=user.age
    )


@router.get("/users", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Tüm kullanıcıları listele (sayfalama ile)."""
    service = GreetingService(db)
    users = service.user_repo.get_all(skip=skip, limit=limit)
    return users


@router.get("/greetings/{username}", response_model=GreetingResponse)
async def get_greeting(username: str, db: Session = Depends(get_db)):
    """Username ile kullanıcıyı karşıla."""
    service = GreetingService(db)

    try:
        return service.get_greeting_by_username(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))