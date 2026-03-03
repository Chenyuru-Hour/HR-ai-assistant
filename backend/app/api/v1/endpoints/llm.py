from fastapi import APIRouter

from app.core.config import get_settings
from app.services.llm_client import LLMClient

router = APIRouter()

@router.get("/ping")
async def llm_ping():
    settings = get_settings()
    client = LLMClient()
    try:
        content = await  client.chat("回复当前时间")
        return {
            "success": True,
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "content": content,
        }
    except RuntimeError as exc:
        return {
            "success": False,
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "error": str(exc),
        }