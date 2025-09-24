from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal, Any

class AccountBase(BaseModel):
    username: str = Field(..., min_length=8)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Literal['admin', 'instructor', 'student']

    @field_validator('role', mode='before')
    @classmethod
    def convert_to_lower(cls, v: Any):
        if isinstance(v, str):
            v = v.lower()
        return v

class Account(AccountBase):
    id: str

class AccountCreate(AccountBase):
    pass

class AccountSignIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class AccountUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=8)
    email: Optional[EmailStr] = None
    role: Optional[Literal['admin', 'instructor', 'student']] = None
    curr_password: str

class PasswordUpdate(BaseModel):
    curr_password: str
    new_password: str = Field(..., min_length=8)

class Response(BaseModel):
    message: str
    has_error: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[dict | list[dict]] = None
