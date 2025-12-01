from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    title = Column(String)
    series = Column(String, index=True, nullable=True)
    volume = Column(Integer, default=9999)
    pages = Column(Integer)
    cover_path = Column(String)  # ruta temporal o bytes guardados
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class Manga(Base):
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    title = Column(String)
    pages = Column(Integer)
    cover_path = Column(String)  # ruta temporal o bytes guardados
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class Manhwa(Base):
    __tablename__ = "manhwa"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    title = Column(String)
    pages = Column(Integer)
    cover_path = Column(String)  # ruta temporal o bytes guardados
    uploaded_at = Column(DateTime, default=datetime.utcnow)