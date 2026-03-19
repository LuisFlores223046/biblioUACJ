"""
BiblioUACJ — Base de datos compartida
Todos los equipos importan desde aquí: from database import get_db, Base
NO modificar este archivo.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

DATABASE_URL = "sqlite:///./bibliouacj.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── MODELOS ───────────────────────────────────────────────────────────────────

class Libro(Base):
    __tablename__ = "libros"
    id          = Column(Integer, primary_key=True, index=True)
    titulo      = Column(String, nullable=False)
    autor       = Column(String, nullable=False)
    isbn        = Column(String, unique=True, nullable=False)
    cantidad    = Column(Integer, default=1)
    disponible  = Column(Boolean, default=True)

class Usuario(Base):
    __tablename__ = "usuarios"
    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String, nullable=False)
    matricula   = Column(String, unique=True, nullable=False)
    email       = Column(String, nullable=False)
    activo      = Column(Boolean, default=True)

class Prestamo(Base):
    __tablename__ = "prestamos"
    id              = Column(Integer, primary_key=True, index=True)
    libro_id        = Column(Integer, ForeignKey("libros.id"), nullable=False)
    usuario_id      = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_prestamo  = Column(DateTime, default=datetime.utcnow)
    fecha_devolucion= Column(DateTime, nullable=True)
    devuelto        = Column(Boolean, default=False)
    multa           = Column(Float, default=0.0)

# ── DEPENDENCIA FastAPI ───────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
