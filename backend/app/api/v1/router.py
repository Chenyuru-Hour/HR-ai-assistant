from fastapi import APIRouter

from app.api.v1.endpoints import health, llm, parse, resume, score

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(parse.router, prefix="/parse", tags=["parse"])
api_router.include_router(score.router, prefix="/score", tags=["score"])
api_router.include_router(llm.router, prefix="/llm",tags=["llm"])
