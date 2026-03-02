from app.core.config import get_settings


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self.provider = settings.llm_provider
        self.api_key = settings.llm_api_key

    async def chat(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("LLM_API_KEY is not configured")
        raise NotImplementedError("LLM provider integration will be implemented next.")
