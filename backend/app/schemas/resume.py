from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    saved_path: str
    file_size: int
    message: str

class ExtractResponse(BaseModel):
    filename: str
    file_type: str
    total_pages: int
    text: str
    text_length: int