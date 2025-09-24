from pydantic import BaseModel, Field
from typing import Optional

class CourseBase(BaseModel):
    title: str = Field(..., min_length=3)
    instructor: str = Field(..., min_length=8)
    duration: int = Field(..., ge=2)

class Course(CourseBase):
    id: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=8)
    instructor: Optional[str] = Field(None, min_length=8)

class Response(BaseModel):
    message: str
    has_error: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[dict | list[dict]] = None
