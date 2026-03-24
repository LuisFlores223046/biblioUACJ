"""
EQUIPO 4 — Módulo: Devoluciones
Requerimientos Iteración 1:
  R4.1 Registrar devolución de un préstamo
  R4.2 Calcular si hay retraso (más de 7 días)
  R4.3 Marcar libro como disponible al devolver
  R4.4 Listar devoluciones del día

Requerimientos Iteración 2:
  R4.5 Calcular multa escalonada al devolver
  R4.6 Listar devoluciones que generaron multa mayor a $0
  R4.7 Contar devoluciones en un rango de fechas
  R4.8 Promedio de días que tardan los usuarios en devolver
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from database import get_db, Prestamo, Libro

router = APIRouter()

# ---------------------------------------------------------------------------
# Función auxiliar para R4.5
# ---------------------------------------------------------------------------
def _calcular_multa(dias: int) -> float:
    if dias <= 7:
        return 0.0
    return (dias - 7) * 5.0


# ---------------------------------------------------------------------------
# R4.1 — Registrar devolución (incluye R4.5: multa escalonada)
# ---------------------------------------------------------------------------
@router.put("/{prestamo_id}", summary="R4.1 Registrar devolución")
def devolver_libro(prestamo_id: int, db: Session = Depends(get_db)):
    # Verificar que el préstamo exista
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # Evitar registrar una devolución duplicada
    if prestamo.fecha_devolucion is not None:
        raise HTTPException(status_code=400, detail="Este préstamo ya fue devuelto")

    # Calcular días transcurridos y multa correspondiente (R4.5)
    ahora = datetime.utcnow()
    dias = (ahora - prestamo.fecha_prestamo).days
    multa = _calcular_multa(dias)

    # Guardar fecha de devolución y multa en el préstamo
    prestamo.fecha_devolucion = ahora
    prestamo.multa = multa

    # Marcar el libro como disponible nuevamente (R4.3)
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    if libro:
        libro.disponible = True

    db.commit()
    db.refresh(prestamo)

    return {
        "prestamo_id": prestamo_id,
        "dias_prestado": dias,
        "con_retraso": dias > 7,
        "multa": multa,
        "fecha_devolucion": prestamo.fecha_devolucion,
    }


# ---------------------------------------------------------------------------
# R4.2 — Calcular retraso (sin cambios)
# ---------------------------------------------------------------------------
@router.get("/{prestamo_id}/retraso", summary="R4.2 Calcular retraso")
def consultar_retraso(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    dias = (datetime.utcnow() - prestamo.fecha_prestamo).days
    return {"dias_prestado": dias, "con_retraso": dias > 7}


# ---------------------------------------------------------------------------
# R4.3 — Marcar libro como disponible (sin cambios)
# ---------------------------------------------------------------------------
@router.patch("/{libro_id}/disponibilidad", summary="R4.3 Marcar libro")
def marcar_disponible(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro.disponible = True
    db.commit()
    return {"libro_id": libro_id, "disponible": libro.disponible}


# ---------------------------------------------------------------------------
# R4.4 — Listar devoluciones del día
# ---------------------------------------------------------------------------
@router.get("/hoy", summary="R4.4 Devoluciones del día")
def devoluciones_hoy(db: Session = Depends(get_db)):
    # Obtener solo préstamos que ya tienen fecha de devolución registrada
    prestamos = db.query(Prestamo).filter(Prestamo.fecha_devolucion.isnot(None)).all()

    # Filtrar los que coincidan con la fecha de hoy (ignorando la hora)
    hoy = date.today()
    resultado = [
        {
            "prestamo_id": p.id,
            "libro_id": p.libro_id,
            "usuario_id": p.usuario_id,
            "multa": p.multa,
            "fecha_devolucion": p.fecha_devolucion,
        }
        for p in prestamos
        if p.fecha_devolucion.date() == hoy
    ]

    return {"total": len(resultado), "devoluciones": resultado}


# ---------------------------------------------------------------------------
# R4.6 — Listar devoluciones con multa mayor a $0
# ---------------------------------------------------------------------------
@router.get("/con-multa", summary="R4.6 Devoluciones con multa > $0")
def devoluciones_con_multa(db: Session = Depends(get_db)):
    # Traer solo préstamos devueltos que generaron multa, de mayor a menor
    prestamos = (
        db.query(Prestamo)
        .filter(
            Prestamo.fecha_devolucion.isnot(None),
            Prestamo.multa > 0,
        )
        .order_by(Prestamo.multa.desc())
        .all()
    )

    resultado = [
        {
            "prestamo_id": p.id,
            "usuario_id": p.usuario_id,
            "libro_id": p.libro_id,
            "dias_prestado": (p.fecha_devolucion - p.fecha_prestamo).days,
            "multa": p.multa,
        }
        for p in prestamos
    ]

    return {"total": len(resultado), "devoluciones": resultado}


# ---------------------------------------------------------------------------
# R4.7 — Contar devoluciones en un rango de fechas
# ---------------------------------------------------------------------------
@router.get("/rango", summary="R4.7 Devoluciones en un rango de fechas")
def devoluciones_por_rango(
    fecha_inicio: date = Query(..., description="Fecha de inicio YYYY-MM-DD"),
    fecha_fin: date = Query(..., description="Fecha de fin YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    # Validar que el rango tenga sentido
    if fecha_inicio > fecha_fin:
        raise HTTPException(status_code=400, detail="fecha_inicio no puede ser posterior a fecha_fin")

    # Convertir a datetime para cubrir todo el día de inicio y el día de fin
    inicio_dt = datetime.combine(fecha_inicio, datetime.min.time())
    fin_dt = datetime.combine(fecha_fin, datetime.max.time())

    total = (
        db.query(Prestamo)
        .filter(
            Prestamo.fecha_devolucion.isnot(None),
            Prestamo.fecha_devolucion >= inicio_dt,
            Prestamo.fecha_devolucion <= fin_dt,
        )
        .count()
    )

    return {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "total_devoluciones": total}


# ---------------------------------------------------------------------------
# R4.8 — Promedio de días que tardan los usuarios en devolver
# Solo considera préstamos ya devueltos (fecha_devolucion no nula)
# ---------------------------------------------------------------------------
@router.get("/promedio-dias", summary="R4.8 Promedio de días para devolver")
def promedio_dias_devolucion(db: Session = Depends(get_db)):
    prestamos_devueltos = (
        db.query(Prestamo)
        .filter(Prestamo.fecha_devolucion.isnot(None))
        .all()
    )

    # Si no hay devoluciones registradas, no se puede calcular el promedio
    if not prestamos_devueltos:
        return {"prestamos_cerrados": 0, "promedio_dias": None}

    dias_lista = [(p.fecha_devolucion - p.fecha_prestamo).days for p in prestamos_devueltos]
    promedio = sum(dias_lista) / len(dias_lista)

    return {"prestamos_cerrados": len(dias_lista), "promedio_dias": round(promedio, 2)}
