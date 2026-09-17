# app/core/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.services.auth_service import AuthService

# Swagger'daki "Authorize" kutusu için şema tanımı (tokenUrl login ucunu gösterir)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Token'ı doğrular ve geçerliyse kullanıcıyı döner.
    Endpoint'lerde Depends(get_current_user) ile kullanılır.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik bilgileri",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    service = AuthService(db)
    user = service.user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user