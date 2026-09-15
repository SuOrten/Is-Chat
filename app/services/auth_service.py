# app/services/auth_service.py

from datetime import timedelta
from sqlalchemy.orm import Session

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(
        self,
        username: str,
        password: str,
        full_name: str,
        email: str | None = None,
        age: int | None = None,
    ):
        """Yeni kullanıcı kaydeder."""
        # Kullanıcı adı müsait mi?
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            raise ValueError("Bu kullanıcı adı zaten alınmış.")

        # Şifreyi hash'le
        hashed = get_password_hash(password)

        # Kullanıcıyı oluştur (repository üzerinden)
        db_user = self.user_repo.create(
            username=username,
            full_name=full_name,
            email=email,
            age=age,
            hashed_password=hashed,
        )
        return db_user

    def authenticate_user(self, username: str, password: str):
        """Kullanıcı adı ve şifreyi doğrular."""
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def login_for_access_token(self, username: str, password: str) -> str:
        """Giriş yapar ve access token döner."""
        user = self.authenticate_user(username, password)
        if not user:
            raise ValueError("Kullanıcı adı veya şifre hatalı.")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},  # 'sub' (subject) alanına username'i koyuyoruz
            expires_delta=access_token_expires,
        )
        return access_token