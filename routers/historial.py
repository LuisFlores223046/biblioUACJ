"""
EQUIPO 6 — Módulo: Historial de Préstamos
Requerimientos:
  R6.1 Ver historial de préstamos de un usuario
  R6.2 Ver historial de préstamos de un libro
  R6.3 Listar todos los préstamos (activos y cerrados)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db, Libro, Usuario, Prestamo

router = APIRouter(
    prefix="",
    tags=["Historial de Préstamos"]
)


@router.get("/")
def listar_historial(db: Session = Depends(get_db)):
    """
    R.1 - Listar todo el historial de préstamos.
    Devuelve todos los préstamos registrados (activos y devueltos).
    """
    prestamos = db.query(Prestamo).all()
    return prestamos


@router.get("/usuario/{usuario_id}")
def historial_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    R.2 - Historial de préstamos de un usuario específico.
    Verifica que el usuario exista antes de consultar.
    """
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
    """
    R.3 - Historial de préstamos de un libro específico.
    Verifica que el libro exista antes de consultar.
    """
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    prestamos = db.query(Prestamo).filter(Prestamo.libro_id == libro_id).all()
    return {
        "libro": libro,
        "prestamos": prestamos,
        "total": len(prestamos)
    }


@router.get("/vencidos")
def prestamos_vencidos(db: Session = Depends(get_db)):
    """
    R.4 - Listar préstamos vencidos.
    Un préstamo está vencido si no ha sido devuelto y su fecha_devolucion
    ya pasó (o tiene multa registrada).
    """
    hoy = date.today()
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