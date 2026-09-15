# app/config.py

import os
from dotenv import load_dotenv

# Proje kökündeki .env dosyasını yükle
load_dotenv()

# Model Garden (İşGPT) ayarları — değerler .env'den gelir, koda gömülmez
MODEL_GARDEN_BASE_URL = os.getenv("MODEL_GARDEN_BASE_URL")
if not MODEL_GARDEN_BASE_URL:
    raise RuntimeError("MODEL_GARDEN_BASE_URL .env içinde tanımlı olmalı")

MODEL_GARDEN_USERNAME = os.getenv("MODEL_GARDEN_USERNAME", "")
MODEL_GARDEN_PASSWORD = os.getenv("MODEL_GARDEN_PASSWORD", "")
CHAT_MODEL = os.getenv("CHAT_MODEL", "Qwen/Qwen3-32B-AWQ")
MODEL_GARDEN_TIMEOUT = int(os.getenv("MODEL_GARDEN_TIMEOUT", "60"))