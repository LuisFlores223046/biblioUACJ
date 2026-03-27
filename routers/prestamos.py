"""
EQUIPO 3 — Módulo: Registro de Préstamos
Requerimientos:
  R3.1 Registrar préstamo (libro_id, usuario_id)
  R3.2 Verificar disponibilidad del libro antes de prestar
  R3.3 Listar préstamos activos
  R3.4 Consultar préstamo por ID
  R3.5 Validación en cadena al registrar
  R3.6 Listar activos del más antiguo al más reciente
  R3.7 Total de préstamos por libro
  R3.8 Préstamos activos con más de 5 días
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
    """R3.5 Validación en cadena: libro existe → disponible → usuario activo → menos de 3 préstamos activos."""
    # Validar que el libro existe
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    if not libro:
        raise HTTPException(status_code=400, detail="Libro no encontrado")

    # Validar que el libro está disponible
    if not libro.disponible:
        raise HTTPException(status_code=400, detail="Libro no disponible")

    # Validar que el usuario existe y está activo
    usuario = db.query(Usuario).filter(Usuario.id == prestamo.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if not usuario.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    # Validar que el usuario tiene menos de 3 préstamos activos
    prestamos_activos = db.query(Prestamo).filter(
        Prestamo.usuario_id == prestamo.usuario_id,
        Prestamo.devuelto == False
    ).count()
    if prestamos_activos >= 3:
        raise HTTPException(status_code=400, detail="El usuario ya tiene 3 préstamos activos")

    # Crear el préstamo
    from datetime import datetime
    nuevo = Prestamo(
        libro_id=prestamo.libro_id,
        usuario_id=prestamo.usuario_id,
        fecha_prestamo=datetime.utcnow(),
        devuelto=False,
        multa=0
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/activos", summary="R3.3 Listar préstamos activos")
def prestamos_activos(db: Session = Depends(get_db)):
    #Lista todos los préstamos activos.
    return db.query(Prestamo).filter(Prestamo.devuelto == False).all()

@router.get("/activos/ordenados", summary="R3.6 Préstamos activos del más antiguo al más reciente")
def prestamos_activos_ordenados(db: Session = Depends(get_db)):
    #Lista préstamos activos ordenados del más antiguo al más reciente.
    prestamos = db.query(Prestamo).filter(
        Prestamo.devuelto == False
    ).order_by(Prestamo.fecha_prestamo.asc()).all()
    return prestamos

@router.get("/activos/vencidos", summary="R3.8 Préstamos activos con más de 5 días")
def prestamos_vencidos(db: Session = Depends(get_db)):
    #Lista préstamos activos que llevan más de 5 días sin devolverse.
    from datetime import datetime, timedelta
    limite = datetime.utcnow() - timedelta(days=5)
    prestamos = db.query(Prestamo).filter(
        Prestamo.devuelto == False,
        Prestamo.fecha_prestamo <= limite
    ).all()
    return prestamos

@router.get("/libro/{libro_id}/total", summary="R3.7 Total de préstamos por libro")
def total_prestamos_libro(libro_id: int, db: Session = Depends(get_db)):
    #Regresa cuántas veces ha sido prestado un libro en total.
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    total = db.query(Prestamo).filter(Prestamo.libro_id == libro_id).count()
    return {"libro_id": libro_id, "total_prestamos": total}

@router.get("/{prestamo_id}", summary="R3.4 Consultar préstamo")
def obtener_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    #Consulta un préstamo por su ID.
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo