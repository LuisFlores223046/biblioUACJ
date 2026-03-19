"""
EQUIPO 3 — Módulo: Registro de Préstamos
Requerimientos:
  R3.1 Registrar préstamo (libro_id, usuario_id)
  R3.2 Verificar disponibilidad del libro antes de prestar
  R3.3 Listar préstamos activos
  R3.4 Consultar préstamo por ID
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Prestamo, Libro, Usuario

router = APIRouter()

class PrestamoCreate(BaseModel):
    libro_id: int
    usuario_id: int

# TODO Equipo 3: Implementar los endpoints ↓

@router.post("/", summary="R3.1 Registrar préstamo")
def crear_prestamo(prestamo: PrestamoCreate, db: Session = Depends(get_db)):
    pass

@router.get("/activos", summary="R3.3 Listar préstamos activos")
def prestamos_activos(db: Session = Depends(get_db)):
    pass

@router.get("/{prestamo_id}", summary="R3.4 Consultar préstamo")
def obtener_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    pass
