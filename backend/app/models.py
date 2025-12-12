from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relación con progreso
    progress = relationship("ReadingProgress", back_populates="user", cascade="all, delete-orphan")

class ReadingProgress(Base):
    __tablename__ = "reading_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comic_id = Column(Integer, ForeignKey("comics.id"))
    current_page = Column(Integer, default=0)
    reading_mode = Column(String, default="double")
    reading_direction = Column(String, default="ltr")

    user = relationship("User", back_populates="progress")
    comic = relationship("Comic")