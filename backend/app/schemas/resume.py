from typing import Optional
from pydantic import BaseModel

# 文件上传/提取相关
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

# 简历结构化数据模型
class BasicInfo(BaseModel):
    """基本信息"""
    name: str
    gender: Optional[str] = None
    age: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    work_years: Optional[str] = None
    education_level: Optional[str] = None
    job_intent: Optional[str] = None

class Education(BaseModel):
    """教育背景"""
    school: str
    major: Optional[str] = None
    degree: Optional[str] = None
    period: Optional[str] = None

class WorkExperience(BaseModel):
    """工作/实习经历"""
    company: str
    position: Optional[str] = None
    period: Optional[str] = None
    description: Optional[str] = None

class Project(BaseModel):
    """项目经历"""
    name: str
    role: Optional[str] = None
    period: Optional[str] = None
    description: Optional[str] = None

class Award(BaseModel):
    """荣誉奖项"""
    name: str
    time: Optional[str] = None

class Certificate(BaseModel):
    """证书/资格证"""
    name: str
    time: Optional[str] = None

class ResumeData(BaseModel):
    """简历结构化数据"""
    basic_info: BasicInfo
    education: list[Education] = []
    work_experience: list[WorkExperience] = []
    projects: list[Project] = []
    skills: list[str] = []
    awards: list[Award] = []
    certificates: list[Certificate] = []
    campus_experience: list[str] = []
    self_evaluation: Optional[str] = None

class ParseResponse(BaseModel):
    """解析接口响应"""
    filename: str
    success: bool
    data: Optional[ResumeData] = None
    error: Optional[str] = None
