# app/schemas/token.py

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Login başarılı olunca dönen token."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token çözüldükten sonra içindeki veri."""
    username: Optional[str] = None

class UserLogin(BaseModel):
    """Login isteği: Kullanıcı adı ve şifre."""
    username: str
    password: str

