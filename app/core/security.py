# app/core/security.py

import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt
import bcrypt


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Düz şifre ile hash'lenmiş şifreyi karşılaştırır.
    bcrypt.checkpw bytes bekler, bu yüzden encode ediyoruz.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Şifreyi hash'ler (karmalar).
    Salt oluştur ve hash'le.
    """
    # rounds=10: Güvenlik ve performans dengesi (test projesi için ideal)
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT token oluşturur."""
    to_encode = data.copy()

    # Süre belirle
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Süre bilgisini ekle
    to_encode.update({"exp": expire})

    # Token'ı oluştur ve döndür
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt