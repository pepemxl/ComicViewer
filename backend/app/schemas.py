from pydantic import BaseModel
from datetime import datetime

class ComicBase(BaseModel):
    filename: str
    title: str

class ComicCreate(ComicBase):
    pass

class ComicResponse(ComicBase):
    id: int
    pages: int
    cover_path: str | None
    uploaded_at: datetime

    class Config:
        from_attributes = True