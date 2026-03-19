"""
EQUIPO 4 — Módulo: Devoluciones
Requerimientos:
  R4.1 Registrar devolución de un préstamo
  R4.2 Calcular si hay retraso (más de 7 días)
  R4.3 Marcar libro como disponible al devolver
  R4.4 Listar devoluciones del día
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db, Prestamo, Libro

router = APIRouter()

# TODO Equipo 4: Implementar los endpoints ↓

@router.put("/{prestamo_id}", summary="R4.1 Registrar devolución")
def devolver_libro(prestamo_id: int, db: Session = Depends(get_db)):
    pass

@router.get("/hoy", summary="R4.4 Devoluciones del día")
def devoluciones_hoy(db: Session = Depends(get_db)):
    pass
