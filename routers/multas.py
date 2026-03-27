"""
EQUIPO 7 — Módulo: Control de Multas
Requerimientos:
  R7.1 Calcular multa de un préstamo (5 pesos por día de retraso)
  R7.2 Ver multas pendientes de un usuario
  R7.3 Registrar pago de multa
  R7.4 Ver total de multas del sistema
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db, Prestamo, Usuario

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


"""
    Devuelve todos los préstamos con multa pendiente de un usuario.
    Una multa está pendiente cuando multa > 0 y el préstamo no fue devuelto,
    o cuando fue devuelto pero la multa registrada aún no se cobró (multa > 0).
"""
@router.get("/usuario/{usuario_id}", summary="R7.2 Multas de usuario")
def multas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    
    """
    Busca al usuario en la BD cuyo id coincida con el parámetro recibido
    first() regresa None si no encontró ningún registro y arroja un HTTPException
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
 
    prestamos = db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id).all()
 
    pendientes = []
    total_pendiente = 0.0
 
    # Recorre cada préstamo del usuario
    for p in prestamos:  
        
        # Si ya fue devuelto usa la fecha de devolución, si no usa la fecha actual
        fecha_ref = p.fecha_devolucion if p.devuelto else datetime.utcnow()
        
        # Calcula cuántos días han pasado desde que se prestó el libro
        dias_transcurridos = (fecha_ref - p.fecha_prestamo).days
        dias_retraso = max(0, dias_transcurridos - DIAS_LIMITE)
        multa_calculada = dias_retraso * COSTO_DIA

        if multa_calculada > 0 and not p.devuelto:
            # Caso 1: préstamo activo y ya tiene retraso
            # Se agrega a la lista con la multa calculada
            pendientes.append({
                "prestamo_id": p.id,
                "libro_id": p.libro_id,
                "fecha_prestamo": p.fecha_prestamo,
                "dias_retraso": dias_retraso,
                "multa_pendiente": multa_calculada,
                "devuelto": p.devuelto,
            })
            total_pendiente += multa_calculada  # Acumula al total
        elif p.multa > 0:
            # Caso 2: préstamo ya devuelto pero con multa registrada sin pagar en la BD
            pendientes.append({
                "prestamo_id": p.id,
                "libro_id": p.libro_id,
                "fecha_prestamo": p.fecha_prestamo,
                "dias_retraso": dias_retraso,
                "multa_pendiente": p.multa,
                "devuelto": p.devuelto,
            })
            total_pendiente += p.multa  # Acumula al total
 
    return {
        "usuario_id": usuario_id,
        "nombre": usuario.nombre,
        "matricula": usuario.matricula,
        "multas_pendientes": pendientes,
        "total_pendiente": total_pendiente,
        "cantidad_multas": len(pendientes),
    }

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
    """Autor: Raúl Esteban Aniles Macias 222802
    # Funcionalidad: Retorna el total acumulado de multas registradas en el sistema.
    """
    total = db.query(Prestamo).with_entities(func.sum(Prestamo.multa)).scalar() or 0.0
    return {"total_multas": float(total)}

@router.get("/calcular_multa/{prestamo_id}", summary="R7.5 Calcular multa")
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

@router.get("/usuarios_conmulta", summary="R7.6 Listar usuarios con multa")
def usuarios_multados(db:Session = Depends(get_db)):
    prestamos = db.query(Prestamo.usuario_id).filter(Prestamo.multa > 0.0).subquery()
    usuarios = db.query(Usuario)\
        .filter(Usuario.id.in_(prestamos)).all() 
    return usuarios
