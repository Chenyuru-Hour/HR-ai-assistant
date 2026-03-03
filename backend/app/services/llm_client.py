import httpx

from app.core.config import get_settings


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self.provider = settings.llm_provider
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.timeout_seconds = settings.llm_timeout_seconds
        self.chat_url = settings.llm_chat_completions_url

    async def chat(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("LLM_API_KEY is not configured")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role":"user","content":prompt}],
            "temperature": 0,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(self.chat_url, headers=headers,json=payload,)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise RuntimeError("LLM request timeout") from exc
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"LLM upstream error: {exc.response.status_code} {exc.response.text}") from exc
        except httpx.HTTPError as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError,IndexError,TypeError) as exc:
            raise RuntimeError(f"Invalid LLM response format: {data}") from exc

