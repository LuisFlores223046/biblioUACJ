"""
EQUIPO 7 — Módulo: Control de Multas
Requerimientos:
  R7.1 Calcular multa de un préstamo (5 pesos por día de retraso)
  R7.2 Ver multas pendientes de un usuario
  R7.3 Registrar pago de multa
  R7.4 Ver total de multas del sistema
"""
from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db, Prestamo

router = APIRouter()

COSTO_DIA = 5.0  # pesos por día de retraso
DIAS_LIMITE = 7  # días antes de generar multa

# TODO Equipo 7: Implementar los endpoints ↓

@router.get("/calcular/{prestamo_id}", summary="R7.1 Calcular multa")
def calcular_multa(prestamo_id: int, db: Session = Depends(get_db)):
    pass

@router.get("/usuario/{usuario_id}", summary="R7.2 Multas de usuario")
def multas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    pass

@router.put("/pagar/{prestamo_id}", summary="R7.3 Registrar pago")
def pagar_multa(prestamo_id: int, db: Session = Depends(get_db)):
    # Obtiene el préstamo por su ID
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    # Valida que el préstamo exista
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    #Valida si se tiene una multa pendiente
    if prestamo.multa <= 0:
        return {"message": "El préstamo no tiene multas pendientes", "multa_actual": prestamo.multa}
    
    #Guarda el monto de la multa antes de pagarla
    monto_pagado = prestamo.multa
    #Registra el pago y actualiza la multa a 0
    prestamo.multa = 0.0

    #Guarda los cambios en la base de datos
    db.commit()
    db.refresh(prestamo)

    #Respuesta con el resultado del pago
    return {"status": "success", "message": f"Multa de {monto_pagado} pagada correctamente","nuevo_saldo_multa": prestamo.multa }

@router.get("/total", summary="R7.4 Total de multas")
def total_multas(db: Session = Depends(get_db)):
    pass
