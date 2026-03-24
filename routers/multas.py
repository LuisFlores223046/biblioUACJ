"""
EQUIPO 7 — Módulo: Control de Multas
Requerimientos:
  R7.1 Calcular multa de un préstamo (5 pesos por día de retraso)
  R7.2 Ver multas pendientes de un usuario
  R7.3 Registrar pago de multa
  R7.4 Ver total de multas del sistema
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db, Prestamo

router = APIRouter()

COSTO_DIA = 5.0  # pesos por día de retraso
DIAS_LIMITE = 7  # días antes de generar multa

# TODO Equipo 7: Implementar los endpoints ↓

from fastapi import HTTPException


@router.get("/calcular/{prestamo_id}", summary="R7.1 Calcular multa")
def calcular_multa(prestamo_id: int, db: Session = Depends(get_db)):
    """
    Autor: Raúl Esteban Aniles Macias 222802
    # Funcionalidad: Calcula la multa de un préstamo según días de retraso (5 pesos/día a partir del día 8).
    """
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if prestamo.devuelto and prestamo.fecha_devolucion:
        fecha_final = prestamo.fecha_devolucion
    else:
        fecha_final = datetime.utcnow()

    dias_prestamo = (fecha_final - prestamo.fecha_prestamo).days
    dias_retraso = dias_prestamo - DIAS_LIMITE
    multa_calculada = max(0, dias_retraso * COSTO_DIA)

    # Guardar multa calculada para persistencia si aún no está actualizada
    if prestamo.multa != multa_calculada:
        prestamo.multa = multa_calculada
        db.add(prestamo)
        db.commit()
        db.refresh(prestamo)

    return {
        "prestamo_id": prestamo_id,
        "dias_prestamo": dias_prestamo,
        "dias_retraso": max(0, dias_retraso),
        "multa": multa_calculada,
        "estado_devuelto": prestamo.devuelto,
        "fecha_devolucion": prestamo.fecha_devolucion,
    }


@router.get("/usuario/{usuario_id}", summary="R7.2 Multas de usuario")
def multas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    pass

@router.put("/pagar/{prestamo_id}", summary="R7.3 Registrar pago")
def pagar_multa(prestamo_id: int, db: Session = Depends(get_db)):
    pass

@router.get("/total", summary="R7.4 Total de multas")
def total_multas(db: Session = Depends(get_db)):
    """Autor: Raúl Esteban Aniles Macias 222802
    # Funcionalidad: Retorna el total acumulado de multas registradas en el sistema.
    """
    total = db.query(Prestamo).with_entities(func.sum(Prestamo.multa)).scalar() or 0.0
    return {"total_multas": float(total)}
