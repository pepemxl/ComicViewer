from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ComicBase(BaseModel):
    filename: str
    title: str

class ComicCreate(ComicBase):
    pass

class ComicResponse(ComicBase):
    id: int
    pages: int
    series: Optional[str] = None
    volume: Optional[int] = None
    cover_path: str | None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
