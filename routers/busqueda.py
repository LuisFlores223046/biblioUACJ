"""
EQUIPO 5 — Módulo: Búsqueda de Libros
Requerimientos:
  R5.1 Buscar libros por título (búsqueda parcial)
  R5.2 Buscar libros por autor
  R5.3 Buscar libros disponibles solamente
  R5.4 Buscar por ISBN exacto
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Libro

router = APIRouter()

# TODO Equipo 5: Implementar los endpoints ↓

@router.get("/titulo/{titulo}", summary="R5.1 Buscar por título")
def buscar_titulo(titulo: str, db: Session = Depends(get_db)):
    pass

@router.get("/autor/{autor}", summary="R5.2 Buscar por autor")
def buscar_autor(autor: str, db: Session = Depends(get_db)):
    pass

@router.get("/disponibles", summary="R5.3 Libros disponibles")
def libros_disponibles(db: Session = Depends(get_db)):
    pass

@router.get("/isbn/{isbn}", summary="R5.4 Buscar por ISBN")
def buscar_isbn(isbn: str, db: Session = Depends(get_db)):
    pass
