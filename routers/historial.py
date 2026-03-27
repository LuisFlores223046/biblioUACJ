"""
EQUIPO 6 — Módulo: Historial de Préstamos
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from database import get_db, Libro, Usuario, Prestamo

router = APIRouter(
    prefix="",
    tags=["Historial de Préstamos"]
)



@router.get("/")
def listar_historial(db: Session = Depends(get_db)):
    prestamos = db.query(Prestamo).all()
    return prestamos



@router.get("/usuario/{usuario_id}")
def historial_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    prestamos = db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id).all()

    return {
        "usuario": usuario,
        "prestamos": prestamos,
        "total": len(prestamos)
    }

@router.get("/libro/{libro_id}")
def historial_por_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    prestamos = db.query(Prestamo).filter(Prestamo.libro_id == libro_id).all()

    return {
        "libro": libro,
        "prestamos": prestamos,
        "total": len(prestamos)
    }



@router.get("/usuario/{usuario_id}/detalle")
def historial_usuario_detallado(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    prestamos = db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id).all()

    resultado = []

    for p in prestamos:
        # Libro seguro
        libro = db.query(Libro).filter(Libro.id == p.libro_id).first()
        titulo = libro.titulo if libro and hasattr(libro, "titulo") else "Desconocido"

        # Validación de fechas
        dias = None
        if p.fecha_prestamo:
            fecha_fin = p.fecha_devolucion if p.fecha_devolucion else datetime.now()
            try:
                dias = (fecha_fin - p.fecha_prestamo).days
            except:
                dias = None

        # Evaluar puntualidad
        a_tiempo = None
        if dias is not None:
            a_tiempo = dias < 7

        resultado.append({
            "libro": titulo,
            "fecha_prestamo": p.fecha_prestamo,
            "dias_prestado": dias,
            "devuelto": p.devuelto,
            "a_tiempo": a_tiempo
        })

    return {
        "usuario": usuario,
        "total": len(resultado),
        "historial": resultado
    }



@router.get("/usuario/{usuario_id}/score")
def score_puntualidad(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    prestamos = db.query(Prestamo).filter(
        Prestamo.usuario_id == usuario_id,
        Prestamo.devuelto == True
    ).all()

    if not prestamos:
        return {
            "usuario": usuario,
            "score": None,
            "mensaje": "El usuario no tiene préstamos cerrados"
        }

    a_tiempo = 0

    for p in prestamos:
        if p.fecha_prestamo and p.fecha_devolucion:
            try:
                dias = (p.fecha_devolucion - p.fecha_prestamo).days
                if dias < 7:
                    a_tiempo += 1
            except:
                continue

    total = len(prestamos)
    score = (a_tiempo / total) * 100 if total > 0 else None

    return {
        "usuario": usuario,
        "prestamos_cerrados": total,
        "a_tiempo": a_tiempo,
        "score": round(score, 2) if score is not None else None
    }



@router.get("/top-libros")
def top_libros(db: Session = Depends(get_db)):
    top = db.query(
        Prestamo.libro_id,
        func.count(Prestamo.id).label("total")
    ).group_by(
        Prestamo.libro_id
    ).order_by(
        func.count(Prestamo.id).desc()
    ).limit(3).all()

    if not top:
        return {"mensaje": "No hay préstamos registrados", "libros": []}

    resultado = []

    for t in top:
        libro = db.query(Libro).filter(Libro.id == t.libro_id).first()

        titulo = "Desconocido"
        if libro and hasattr(libro, "titulo"):
            titulo = libro.titulo

        resultado.append({
            "libro": titulo,
            "veces_prestado": t.total
        })

    return {
        "total": len(resultado),
        "top": resultado
    }



@router.get("/ordenado")
def historial_ordenado(db: Session = Depends(get_db)):
    prestamos = db.query(Prestamo).order_by(
        Prestamo.fecha_prestamo.desc().nullslast()
    ).all()

    if not prestamos:
        return {"mensaje": "No hay historial", "total": 0, "prestamos": []}

    return {
        "total": len(prestamos),
        "prestamos": prestamos
    }



@router.get("/vencidos")
def prestamos_vencidos(db: Session = Depends(get_db)):
    hoy = datetime.now()

    vencidos = db.query(Prestamo).filter(
        Prestamo.devuelto == False,
        Prestamo.fecha_devolucion != None,
        Prestamo.fecha_devolucion < hoy
    ).all()

    if not vencidos:
        return {"mensaje": "No hay préstamos vencidos", "total": 0, "prestamos": []}

    return {
        "total": len(vencidos),
        "prestamos": vencidos
    }