# app/services/greeting_service.py

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import GreetingResponse


class GreetingService:
    """Karşılama iş mantığı."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def create_greeting(self, username: str) -> GreetingResponse:
        """Kullanıcıyı karşıla."""
        if username.lower() == "charlie":
            raise ValueError("Bu kullanıcı yasaklıdır. Erişim engellendi.")

        user = self.user_repo.get_by_username(username)

        if user is None:
            raise ValueError(f"Kullanıcı bulunamadı: {username}")

        if user.username == "bob":
            message = f"Selam {user.full_name}! Özel bir karşılama: Hoş geldin!"
        else:
            message = f"Merhaba {user.full_name}! Sisteme hoş geldin, {user.username}!"

        return GreetingResponse(
            message=message,
            user_id=user.id,
            full_name=user.full_name,
            email=user.email
        )

    def get_greeting_by_username(self, username: str) -> GreetingResponse:
        """Username ile kullanıcı bul ve karşıla."""
        user = self.user_repo.get_by_username(username)

        if user is None:
            raise ValueError(f"Kullanıcı bulunamadı: {username}")

        if user.username == "bob":
            message = f"Selam {user.full_name}! Özel bir karşılama: Hoş geldin!"
        else:
            message = f"Merhaba {user.full_name}! Sisteme hoş geldin, {user.username}!"

        return GreetingResponse(
            message=message,
            user_id=user.id,
            full_name=user.full_name,
            email=user.email
        )