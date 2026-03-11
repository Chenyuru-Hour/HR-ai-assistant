from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.resume import ExtractResponse, ParseResponse
from app.services.file_parser import parse_file
from app.services.resume_parser import parse_resume


router = APIRouter()

class ExtractRequest(BaseModel):
    """文本提取请求参数"""
    file_path: str

@router.post("/extract", response_model=ExtractResponse)
async def extract_text(request: ExtractRequest):
    """从已上传的简历文件中提取文本"""

    # 1.校验文件是否存在
    path = Path(request.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"文件不存在：{request.file_path}")

    # 2.获取文件类型
    file_ext = path.suffix.lower()
    if file_ext == ".pdf":
        file_type = "pdf"
    elif file_ext == ".docx":
        file_type = "docx"
    else:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型：{file_ext}")

    # 3.调用解析服务提取文本
    try:
        result = parse_file(str(path), file_type)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"文本提取失败：{exc}")

    # 4.返回提取结果
    return ExtractResponse(
        filename=path.name,
        file_type=file_type,
        total_pages=result["total_pages"],
        text=result["text"],
        text_length=len(result["text"])
    )

@router.post("/analyze", response_model=ParseResponse)
async def analyze_resume(request: ExtractRequest):
    """AI解析简历：提取文本以及结构化解析"""

    # 1.校验文件是否存在
    path = Path(request.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"文件不存在：{request.file_path}")

    # 2.获取文件类型
    file_ext = path.suffix.lower()
    if file_ext == ".pdf":
        file_type = "pdf"
    elif file_ext == ".docx":
        file_type = "docx"
    else:
        raise HTTPException(status_code=400,detail=f"不支持的文件类型：{file_ext}")

    # 3.提取文本
    try:
        extract_result = parse_file(str(path), file_type)
    except Exception as exc:
        return ParseResponse(
            filename=path.name,
            success=False,
            error=f"文本提取失败：{exc}"
        )

    # 4.调用AI解析
    try:
        resume_data = await parse_resume(extract_result["text"])
    except Exception as exc:
        return ParseResponse(
            filename=path.name,
            success=False,
            error=f"AI解析失败：{exc}"
        )

    # 5.返回解析结果
    return ParseResponse(
        filename=path.name,
        success=True,
        data=resume_data
    )

@router.get("/ping")
async def parse_ping():
    return {"module": "parse", "status": "todo"}
