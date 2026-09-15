# app/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional


class UserRepository:
    """
    Kullanıcı veritabanı işlemleri.

    Sadece SQL sorguları burada yazılır.
    Service katmanı bu class'ı kullanır, SQL bilmez.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, full_name: str, email: str | None, age: int | None,
               hashed_password: str) -> User:
        """
        Yeni kullanıcı oluştur.
        """
        db_user = User(
            username=username,
            full_name=full_name,
            email=email,
            age=age,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Username ile kullanıcı bul.
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        ID ile kullanıcı bul.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self, skip: int = 0, limit: int = 10):
        """
        Tüm kullanıcıları listele (sayfalama ile).
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def delete(self, user_id: int) -> bool:
        """
        Kullanıcıyı sil.
        """
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False