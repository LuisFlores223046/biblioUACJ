"""
EQUIPO 6 — Módulo: Historial de Préstamos
Requerimientos:
  R6.1 Ver historial de préstamos de un usuario
  R6.2 Ver historial de préstamos de un libro
  R6.3 Listar todos los préstamos (activos y cerrados)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Prestamo

router = APIRouter()

# TODO Equipo 6: Implementar los endpoints ↓

@router.get("/usuario/{usuario_id}", summary="R6.1 Historial de usuario")
def historial_usuario(usuario_id: int, db: Session = Depends(get_db)):
    pass

@router.get("/libro/{libro_id}", summary="R6.2 Historial de libro")
def historial_libro(libro_id: int, db: Session = Depends(get_db)):
    pass

@router.get("/todos", summary="R6.3 Todos los préstamos")
def todos_prestamos(db: Session = Depends(get_db)):
    pass
