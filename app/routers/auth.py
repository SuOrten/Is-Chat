# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user   # taşınan dependency
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydeder."""
    service = AuthService(db)
    try:
        user = service.register_user(
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name,
            email=user_data.email,
            age=user_data.age
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            age=user.age
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Giriş yap ve token al."""
    service = AuthService(db)
    try:
        token = service.login_for_access_token(
            username=form_data.username,
            password=form_data.password
        )
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    """Kendi kullanıcı bilgilerini getir. Sadece giriş yapmış kullanıcılar erişebilir."""
    return current_user