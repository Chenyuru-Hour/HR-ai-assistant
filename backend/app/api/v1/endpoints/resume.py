import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, HTTPException

from app.schemas.resume import UploadResponse

router = APIRouter()

# 允许的文件类型
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
# 文件限制大小： 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024
# 上传目录
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent.parent / "uploads"

@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile):
    """上传简历文件"""

    # 1.校验文件名
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    # 2.校验文件类型
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型：{file_ext}, 仅支持 .pdf 和 .docx"
        )

    # 3.读取文件内容
    content = await file.read()

    # 4.校验文件大小
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制：{file_size} 字节，最大允许 {MAX_FILE_SIZE} 字节"
        )

    # 5.确保上传目录存在
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 6.生成唯一文件名并保存
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    save_path = UPLOAD_DIR / unique_filename

    with open(save_path, "wb") as f:
        f.write(content)

    # 7.返回上传结果
    return UploadResponse(
        filename=file.filename,
        saved_path=str(save_path),
        file_size=file_size,
        message="上传成功"
    )

@router.get("/ping")
async def resume_ping():
    return {"module": "resume", "status": "todo"}
