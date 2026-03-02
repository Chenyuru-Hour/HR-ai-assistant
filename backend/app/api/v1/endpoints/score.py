from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def score_ping():
    return {"module": "score", "status": "todo"}
