from sqlalchemy.orm import Session
from . import models, schemas
from .utils import save_comic_file, extract_pages_list
import os

def create_comic(db: Session, file_content: bytes, filename: str):
    filepath = save_comic_file(file_content, filename)
    pages = extract_pages_list(filepath)

    comic = models.Comic(
        filename=filename,
        title=os.path.splitext(filename)[0],
        pages=len(pages)
    )
    db.add(comic)
    db.commit()
    db.refresh(comic)
    return comic

def get_comics(db: Session, skip: int = 0, limit: int = 100):
    #return db.query(models.Comic).offset(skip).limit(limit).all()
    return db.query(models.Comic).order_by(
            models.Comic.series.asc(), 
            models.Comic.volume.asc()
        ).offset(skip).limit(limit).all()

def get_comic(db: Session, comic_id: int):
    return db.query(models.Comic).filter(models.Comic.id == comic_id).first()