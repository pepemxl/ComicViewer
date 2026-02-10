from contextlib import asynccontextmanager
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import Header
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from pathlib import Path
import re
from sqlalchemy.orm import Session
from zipfile import BadZipFile

from . import crud, models, schemas
from .auth import verify_password, get_password_hash, create_access_token, decode_token
from .database import SessionLocal, engine, Base
from .utils import extract_pages_list, get_page_image_with_raise, get_page_image
from .crud import get_comic
#from .schemas import UserCreate, UserResponse
from .schemas import UserCreate, UserResponse, Token


COMICS_ROOT = Path("../comics")   # cambiar en Docker a volumen
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: escanear al iniciar
    db = SessionLocal()
    try:
        scan_comics_library(db)
    finally:
        db.close()
    
    # Shutdown: opcional, aquí puedes limpiar caché si quieres
    yield
    
    # Cleanup si es necesario
    pass

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

def scan_comics_library(db: Session):
    if not COMICS_ROOT.exists():
        print("⚠️  Carpeta /comics no existe - crea el volumen Docker")
        return
    added = 0
    for cbz_path in COMICS_ROOT.rglob("*.cbz"):
        relative = cbz_path.relative_to(COMICS_ROOT).as_posix()
        existing = db.query(models.Comic).filter(models.Comic.filename == relative).first()
        if not existing:
            # Extraer serie del nombre de carpeta padre
            # series = cbz_path.parent.name
            series = cbz_path.parent.name if cbz_path.parent.name != "comics" else "Sin serie"
            title = cbz_path.stem
            vol = extract_volume(title)
            pages = len(extract_pages_list(str(cbz_path)))
            
            comic = models.Comic(
                filename=relative,
                title=title,
                series=series,
                volume=vol,
                pages=pages
            )
            db.add(comic)
            added += 1
    if added > 0:
        db.commit()
        print(f"✅ Añadidos {added} cómics nuevos")
    else:
        print("ℹ️  No hay cómics nuevos")


def run_scan_with_new_db():
    db = SessionLocal()
    try:
        scan_comics_library(db)
    finally:
        db.close()

@app.post("/scan")
async def manual_scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scan_with_new_db)
    return {"status": "escaneando en background..."}



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_token(token)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(401, "Usuario no encontrado")
    return user

# Registro
@app.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(400, "Email ya registrado")
    hashed = get_password_hash(user_in.password)
    user = models.User(email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login
# @app.post("/login")
# def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == form.username).first()
#     if not user or not verify_password(form.password, user.hashed_password):
#         raise HTTPException(401, "Credenciales inválidas")
#     token = create_access_token({"sub": str(user.id)})
#     return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Credenciales inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Guardar/Obtener progreso
@app.post("/progress/{comic_id}")
def save_progress(comic_id: int, progress: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    prog = db.query(models.ReadingProgress).filter(
        models.ReadingProgress.user_id == user.id,
        models.ReadingProgress.comic_id == comic_id
    ).first()
    if not prog:
        prog = models.ReadingProgress(user_id=user.id, comic_id=comic_id)
        db.add(prog)
    prog.current_page = progress.get("current", 0)
    prog.reading_mode = progress.get("reading_mode", "double")
    prog.reading_direction = progress.get("reading_direction", "ltr")
    db.commit()
    return {"status": "ok"}

@app.get("/progress/{comic_id}")
def get_progress(comic_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    prog = db.query(models.ReadingProgress).filter(
        models.ReadingProgress.user_id == user.id,
        models.ReadingProgress.comic_id == comic_id
    ).first()
    if not prog:
        return {"current": 0, "reading_mode": "double", "reading_direction": "ltr"}
    return {
        "current": prog.current_page,
        "reading_mode": prog.reading_mode,
        "reading_direction": prog.reading_direction
    }