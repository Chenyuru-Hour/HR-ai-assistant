from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.services.llm_client import LLMClient

router = APIRouter()

@router.post("/test")
async def llm_test():
    settings = get_settings()
    client = LLMClient()
    try:
        content = await client.chat("请回复：连接成功")
        return {
            "success": True,
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "content": content,
        }
    except RuntimeError as exc:
        return JSONResponse(
            status_code=502,
            content={
                "success": False,
                "provider": settings.llm_provider,
                "model": settings.llm_model,
                "error": str(exc),
            },
        )
    finally:
        await client.close()