from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base
from .utils import extract_pages_list, get_page_image_with_raise, get_page_image
import os
from zipfile import BadZipFile

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CBZ Reader")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload", response_model=schemas.ComicResponse)
async def upload_cbz(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".cbz"):
        raise HTTPException(400, "Solo archivos .cbz")
    
    content = await file.read()
    comic = crud.create_comic(db, content, file.filename)
    return comic

@app.get("/comics")
def list_comics(db: Session = Depends(get_db)):
    return crud.get_comics(db)

@app.get("/comics/{comic_id}/pages")
def comic_pages(comic_id: int, db: Session = Depends(get_db)):
    comic = crud.get_comic(db, comic_id)
    if not comic:
        raise HTTPException(404, "Cómic no encontrado")
    
    filepath = os.path.join(os.path.dirname(__file__), "../../comics", comic.filename)
    return {"pages": extract_pages_list(filepath)}

@app.get("/comics/{comic_id}/page/{page_index}")
def get_page(comic_id: int, page_index: int, db: Session = Depends(get_db)):
    comic = crud.get_comic(db, comic_id)
    if not comic:
        raise HTTPException(404, "Cómic no encontrado")
    
    filepath = os.path.join(os.path.dirname(__file__), "../../comics", comic.filename)
    pages = extract_pages_list(filepath)
    
    if page_index < 0 or page_index >= len(pages):
        raise HTTPException(404, "Página fuera de rango")
    
    #image_io = get_page_image(filepath, pages[page_index])
    try:
        image_io = get_page_image_with_raise(filepath, pages[page_index])
        return StreamingResponse(image_io, media_type="image/jpeg")
    except BadZipFile as e:
        raise HTTPException(404, "Cómic con errores")