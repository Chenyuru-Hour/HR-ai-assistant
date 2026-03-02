from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def resume_ping():
    return {"module": "resume", "status": "todo"}
