"""
EQUIPO 8 — Módulo: Inventario y Disponibilidad
Requerimientos:
  R8.1 Ver inventario completo con disponibilidad
  R8.2 Ver libros con stock bajo (menos de 2 disponibles)
  R8.3 Actualizar cantidad de un libro
  R8.4 Ver resumen del inventario (total libros, disponibles, prestados)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Libro, Prestamo

router = APIRouter()

# TODO Equipo 8: Implementar los endpoints ↓

@router.get("/", summary="R8.1 Inventario completo")
def inventario_completo(db: Session = Depends(get_db)):
    pass

@router.get("/stock-bajo", summary="R8.2 Libros con stock bajo")
def stock_bajo(db: Session = Depends(get_db)):
    pass

@router.put("/{libro_id}/cantidad", summary="R8.3 Actualizar cantidad")
def actualizar_cantidad(libro_id: int, cantidad: int, db: Session = Depends(get_db)):
    pass

@router.get("/resumen", summary="R8.4 Resumen del inventario")
def resumen_inventario(db: Session = Depends(get_db)):
    pass
