# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base

# SQLite veritabanı (dosya tabanlı, kurulum gerektirmez)
# Gerçek projede: PostgreSQL, MySQL gibi bir veritabanı kullanılır
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite için gerekli
)

# SessionLocal = Her istek için yeni bir veritabanı oturumu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency: Her istek için yeni DB oturumu açar.
    İstek bitince otomatik kapatır.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Veritabanı tablolarını oluştur.
    İlk çalıştırmada çağrılır.
    """
    Base.metadata.create_all(bind=engine)