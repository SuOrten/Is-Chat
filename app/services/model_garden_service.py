# app/services/model_garden_service.py

import httpx

from app.config import (
    CHAT_MODEL,
    MODEL_GARDEN_BASE_URL,
    MODEL_GARDEN_PASSWORD,
    MODEL_GARDEN_TIMEOUT,
    MODEL_GARDEN_USERNAME,
)


class ModelGardenService:
    """
    Model Garden'daki Qwen modeline istek gönderen istemci.

    Dış dünyayla (harici API) tüm iletişim service katmanında yapılır;
    router'da HTTP çağrısı yok (katmanlı mimari kuralı).
    """

    def __init__(self):
        self.base_url = MODEL_GARDEN_BASE_URL
        self.model = CHAT_MODEL
        # Basic Auth: sicil/ortak hesap + şifre (.env'den gelir, koda gömülmez)
        self.auth = httpx.BasicAuth(MODEL_GARDEN_USERNAME, MODEL_GARDEN_PASSWORD)

    async def generate_response(self, user_message: str, system_prompt: str | None = None) -> str:
        """
        Kullanıcı mesajını Qwen'e iletir ve modelin cevabını döner.

        - verify=False: kurumsal CA / revocation engeli için (terminaldeki --ssl-no-revoke karşılığı).
          Sadece iç (UAT) ortamlar için; prod'da kurumsal CA doğrulaması açılmalı.
        """
        if system_prompt is None:
            system_prompt = "Kullanıcının verdiği içeriğe göre Türkçe cevap veren bir asistansın. Sadece Türkçe konuş."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 512,
            "temperature": 0,
            "stream": False,
            "chat_template_kwargs": {"enable_thinking": False},
        }

        url = f"{self.base_url}/chat/completions"

        async with httpx.AsyncClient(verify=False, auth=self.auth, timeout=MODEL_GARDEN_TIMEOUT) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()  # 4xx/5xx gelirse exception fırlat
            data = response.json()

        # OpenAI uyumlu yanıt formatı: choices[0].message.content
        return data["choices"][0]["message"]["content"]