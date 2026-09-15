# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite Veritabanı (Dosya tabanlı, kurulum gerektirmez)
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite için gerekli ayar
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency: Her istek için DB oturumu açar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Tabloları oluştur."""
    Base.metadata.create_all(bind=engine)