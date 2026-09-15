# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.token import Token, UserLogin
from app.schemas.user import UserCreate, UserResponse
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/api/v1", tags=["Authentication"])

# OAuth2 şema tanımlaması (Swagger UI için)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


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
    """
    Giriş yap ve token al.

    **username**: Kullanıcı adı
    **password**: Şifre
    """
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


# --- Dependency: Token Doğrulama ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Token'ı doğrular ve geçerliyse kullanıcıyı döner.
    Bu fonksiyon bir 'Dependency'dir, endpoint'lerde Depends() ile kullanılır.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik bilgileri",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Token'ı çöz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Kullanıcıyı bul
    service = AuthService(db)  # Veya direkt UserRepository kullanabiliriz
    user = service.user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


# --- Örnek: Korumalı Endpoint ---
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Kendi kullanıcı bilgilerini getir.
    Sadece giriş yapmış kullanıcılar erişebilir.
    """
    return current_user