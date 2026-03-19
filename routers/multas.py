"""
EQUIPO 7 — Módulo: Control de Multas
Requerimientos:
  R7.1 Calcular multa de un préstamo (5 pesos por día de retraso)
  R7.2 Ver multas pendientes de un usuario
  R7.3 Registrar pago de multa
  R7.4 Ver total de multas del sistema
"""
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
    pass

@router.get("/total", summary="R7.4 Total de multas")
def total_multas(db: Session = Depends(get_db)):
    pass
