# app/main.py

from fastapi import FastAPI
from app.database import init_db
from app.routers import greetings, auth,chat

app = FastAPI(
    title="Mini Chatbot Practice API",
    description="Router/Service/Repository pattern öğrenme projesi",
    version="1.0.0"
)

# Veritabanı tablolarını oluştur
init_db()

app.include_router(greetings.router)
app.include_router(auth.router)  # Auth endpoint'lerini ekle
app.include_router(chat.router)

# Router'ı kaydet



@app.get("/")
async def root():
    """
    API'nin çalıştığını test etmek için.
    """
    return {
        "message": "API çalışıyor!",
        "docs": "/docs",
        "endpoints": [
            "POST /api/v1/users",
            "POST /api/v1/greetings",
            "GET /api/v1/users/{user_id}",
            "GET /api/v1/users"
        ]
    }


@app.get("/health")
async def health_check():
    """
    Sağlık kontrolü.
    """
    return {"status": "healthy"}