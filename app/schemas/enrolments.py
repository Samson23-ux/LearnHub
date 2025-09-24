from pydantic import BaseModel, Field
from typing import Optional

class EnrolBase(BaseModel):
    course_title: str = Field(..., min_length=6)
    course_instructor: str = Field(..., min_length=8)
    student: str = Field(..., min_length=8)

class Enrol(EnrolBase):
    id: str

class EnrolCreate(EnrolBase):
    pass

class Response(BaseModel):
    message: str
    has_error: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[dict | list[dict]] = None
