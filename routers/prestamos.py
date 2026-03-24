"""
EQUIPO 3 — Módulo: Registro de Préstamos
Requerimientos:
  R3.1 Registrar préstamo (libro_id, usuario_id)
  R3.2 Verificar disponibilidad del libro antes de prestar
  R3.3 Listar préstamos activos
  R3.4 Consultar préstamo por ID
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
    #Verificar que el usuario exista
    usuario = db.query(Usuario).filter(Usuario.id == prestamo.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    #Verificar que el usuario esté activo
    if not usuario.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    #Verificar disponibilidad del libro 
    prestamo_existente = db.query(Prestamo).filter(
        Prestamo.libro_id == prestamo.libro_id,
        Prestamo.devuelto == False
    ).first()

    if prestamo_existente:
        raise HTTPException(status_code=400, detail="El libro ya está prestado")

    #Crear préstamo
    nuevo_prestamo = Prestamo(
        libro_id=prestamo.libro_id,
        usuario_id=prestamo.usuario_id,
        fecha_prestamo=datetime.now(),
        fecha_devolucion=None,
        devuelto=False,
        multa=0
    )

    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)

    return nuevo_prestamo

@router.get("/activos", summary="R3.3 Listar préstamos activos")
def prestamos_activos(db: Session = Depends(get_db)):
    # Obtiene los préstamos no devueltos
    prestamos = db.query(Prestamo).filter(Prestamo.devuelto == False).all()
    # Verificar si hay resultados
    if not prestamos:
        raise HTTPException(status_code=404, detail="No hay préstamos activos")
    # Devuelve los préstamos
    return prestamos

@router.get("/{prestamo_id}", summary="R3.4 Consultar préstamo")
def obtener_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo
