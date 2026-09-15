# Is-Chat

IsGPT Model Garden'dan bir model kullanan basit bir FastAPI chatbot backend'i.
Router / Service / Repository / Model katmanlı mimari ile yazıldı.

## Kurulum

1. Sanal ortam oluştur ve aktifleştir:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
2. Bağımlılıkları kur:   
    ```bash
    pip install -r requirements.txt
   



3. env.example dosyasını .env olarak kopyala ve değerleri doldur.

4. Uygulamayı başlat:
    ```bash
    uvicorn app.main:app --reload
    
5. Swagger arayüzü: http://127.0.0.1:8000/docs







## Proje Yapısı

```
CChatbotProject/
├── app/
│   ├── core/          # Güvenlik (JWT, bcrypt), ortak dependency'ler
│   ├── models/        # SQLAlchemy ORM modelleri
│   ├── repositories/  # Veritabanı erişimi (SQL burada)
│   ├── routers/       # HTTP endpoint'leri (SQL/iş mantığı yok)
│   ├── schemas/       # Pydantic DTO'ları (request/response)
│   ├── services/      # İş mantığı (Model Garden çağrısı dahil)
│   ├── config.py      # Yapılandırma (.env'den okur)
│   ├── database.py    # DB bağlantısı
│   └── main.py        # Uygulama girişi
├── .env               # Gizli değerler (repo'ya YÜKLENMEZ)
├── .env.example       # Değişken şablonu
├── .gitignore
├── requirements.txt
└── README.md
```


## Bilinen eksikler
1. PostgreSQL/Docker geçişi henüz yapılmadı (şu an SQLite).
2. conversation / message modelleri ve ilişkiler hazır değil.
3. Alembic migrasyonları, otomatik testler ve CI eksik.