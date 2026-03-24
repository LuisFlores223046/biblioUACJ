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

@router.get("/{prestamo_id}/retraso", summary="R4.2 Calcular retraso")
def consultar_retraso(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    dias = (datetime.utcnow() - prestamo.fecha_prestamo).days
    return {"dias_prestado": dias, "con_retraso": dias > 7}

@router.patch("/{libro_id}/disponibilidad", summary="R4.3 Marcar libro")
def marcar_disponible(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro.disponible = True
    db.commit()
    return {"libro_id": libro_id, "disponible": libro.disponible}

@router.get("/hoy", summary="R4.4 Devoluciones del día")
def devoluciones_hoy(db: Session = Depends(get_db)):
    pass
