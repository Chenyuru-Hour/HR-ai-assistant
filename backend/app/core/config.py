from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HR AI Assistant Backend"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    api_v1_prefix: str = "/api/v1"

    cors_allow_origins: str = "*"

    llm_provider: str = "deepseek"
    llm_base_url: str = "https://runanytime.hxi.me"
    llm_api_key: str = ""
    llm_model: str = "deepseek/deepseek-v3.2"
    llm_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        raw = self.cors_allow_origins.strip()
        if raw == "*":
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    @property
    def llm_chat_completions_url(self) -> str:
        return  f"{self.llm_base_url.rstrip('/')}/v1/chat/completions"


@lru_cache
def get_settings() -> Settings:
    return Settings()
