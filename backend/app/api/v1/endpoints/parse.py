from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def parse_ping():
    return {"module": "parse", "status": "todo"}
