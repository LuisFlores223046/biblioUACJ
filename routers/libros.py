"""
EQUIPO 1 — Módulo: Gestión de Libros
Requerimientos:
  R1.1 Registrar un libro (titulo, autor, isbn, cantidad)
  R1.2 Consultar todos los libros
  R1.3 Consultar un libro por ID
  R1.4 Actualizar datos de un libro
  R1.5 Eliminar un libro
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Libro

router = APIRouter()

class LibroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    cantidad: int = 1

# TODO Equipo 1: Implementar los endpoints ↓

@router.post("/", summary="R1.1 Registrar libro")
def crear_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    # Implementar aquí
    pass

@router.get("/", summary="R1.2 Listar todos los libros")
def listar_libros(db: Session = Depends(get_db)):
    # Implementar aquí
    pass

@router.get("/{libro_id}", summary="R1.3 Consultar libro por ID")
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    # Implementar aquí
    pass

@router.put("/{libro_id}", summary="R1.4 Actualizar libro")
def actualizar_libro(libro_id: int, libro: LibroCreate, db: Session = Depends(get_db)):
    # Implementar aquí
    pass

@router.delete("/{libro_id}", summary="R1.5 Eliminar libro")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    # Implementar aquí
    pass
