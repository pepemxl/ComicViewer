from contextlib import asynccontextmanager
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import os
from pathlib import Path
import re
from sqlalchemy.orm import Session
from zipfile import BadZipFile

from . import crud, models, schemas
from .database import SessionLocal, engine, Base
from .utils import extract_pages_list, get_page_image_with_raise, get_page_image


COMICS_ROOT = Path("../comics")   # cambiar en Docker a volumen
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup events
    print("Application starting up...")
    yield
    # Shutdown events
    print("Application shutting down...")

#app = FastAPI(title="CBZ Reader")
# app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
app = FastAPI(title="CBZ Reader", lifespan=lifespan)


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


def extract_volume(filename: str):
    patterns = [
        r"(?i)(?:vol\.?|volume|tomo)[\s._-]*(\d+)",
        r"(?i)#?(\d+)",
        r"(?i)cap[\s._-]*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
    return 9999

def scan_comics_library():
    if not COMICS_ROOT.exists():
        return
    for cbz_path in COMICS_ROOT.rglob("*.cbz"):
        relative = cbz_path.relative_to(COMICS_ROOT).as_posix()
        # existing = db.query(models.Comic).filter(models.Comic.filename == relative).first()
        existing = False
        if not existing:
            # Extraer serie del nombre de carpeta padre
            series = cbz_path.parent.name
            title = cbz_path.stem
            vol = extract_volume(title)
            
            comic = models.Comic(
                filename=relative,
                title=title,
                series=series,
                volume=vol,
                pages=len(extract_pages_list(str(cbz_path)))
            )
#             db.add(comic)
#     db.commit()



# @app.on_event("startup")
# async def startup_event():
#     # Escanear al iniciar
#     scan_comics_library()



# @app.post("/scan")
# async def manual_scan(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     background_tasks.add_task(scan_comics_library)
#     return {"status": "escaneando..."}