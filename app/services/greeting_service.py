# app/services/greeting_service.py

from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.user import GreetingResponse, UserCreate, UserResponse


class GreetingService:
    """Karşılama iş mantığı."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Yeni kullanıcı oluştur."""
        # Username kontrolü
        existing_user = self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise ValueError(f"Kullanıcı adı zaten kullanılıyor: {user_data.username}")

        # Şifreyi hash'le
        hashed = get_password_hash(user_data.password)

        # Kullanıcı oluştur
        db_user = self.user_repo.create(
            username=user_data.username,
            full_name=user_data.full_name,
            email=user_data.email,
            age=user_data.age,                      # ← eksikti
            hashed_password=hashed,                 # ← eksikti
        )

        # DTO'ya çevir ve döndür
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            full_name=db_user.full_name,
            email=db_user.email,
            age=db_user.age,                        # ← eksikti
        )

    def create_greeting(self, username: str) -> GreetingResponse:

        """
            Kullanıcıyı karşıla.
            """
        # YENİ: Yasaklı kullanıcı kontrolü
        if username.lower() == "charlie":
            raise ValueError("Bu kullanıcı yasaklıdır. Erişim engellendi.")

        """
        Kullanıcıyı karşıla.
        """
        user = self.user_repo.get_by_username(username)

        if user is None:
            raise ValueError(f"Kullanıcı bulunamadı: {username}")

        # İş mantığı: Özel mesajlar
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
        """
        Username ile kullanıcı bul ve karşıla.

        İş mantığı:
        - Kullanıcı yoksa hata fırlat
        - Bob'a özel mesaj
        - Diğerlerine normal mesaj
        """
        user = self.user_repo.get_by_username(username)

        if user is None:
            raise ValueError(f"Kullanıcı bulunamadı: {username}")

        # İş mantığı: Özel mesajlar
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