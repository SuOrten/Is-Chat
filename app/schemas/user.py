# app/schemas/user.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# --- Kullanıcı İçin Şemalar ---
class UserCreate(BaseModel):
    """Yeni kullanıcı oluştururken gelecek istek."""
    username: str = Field(..., min_length=3, max_length=50, description="Kullanıcı adı (3-50 karakter)")
    full_name: str = Field(..., min_length=2, max_length=100, description="Ad Soyad")
    email: str | None = Field(None, description="E-posta adresi (opsiyonel)")
    password: str = Field(..., min_length=6, description="Şifre (en az 6 karakter)")
    age: int | None = None


class UserResponse(BaseModel):
    """Kullanıcı bilgisi dönerken kullanılacak cevap."""
    id: int
    username: str
    full_name: str
    email: str | None = None
    age: int | None = None

    model_config = ConfigDict(from_attributes=True)


# --- Greeting İçin Şemalar ---
class GreetingRequest(BaseModel):
    """Karşılama için istek."""
    username: str = Field(..., min_length=3, max_length=50)


class GreetingResponse(BaseModel):
    """Karşılama cevabı."""
    message: str
    user_id: int
    full_name: str
    email: str | None = None