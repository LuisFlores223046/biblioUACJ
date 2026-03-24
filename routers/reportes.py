"""
EQUIPO 9 — Módulo: Reportes y Estadísticas
Requerimientos:
  R9.1 Top 5 libros más prestados
  R9.2 Usuarios con más préstamos activos
  R9.3 Reporte de préstamos por fecha
  R9.4 Estadísticas generales del sistema
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Prestamo, Libro, Usuario

router = APIRouter()

# TODO Equipo 9: Implementar los endpoints ↓

@router.get("/top-libros", summary="R9.1 Top 5 libros más prestados")
def top_libros(db: Session = Depends(get_db)):
    pass

@router.get("/usuarios-activos", summary="R9.2 Usuarios con más préstamos")
def usuarios_activos(db: Session = Depends(get_db)):
    pass

@router.get("/por-fecha", summary="R9.3 Préstamos por fecha")
def prestamos_por_fecha(fecha: str, db: Session = Depends(get_db)):
    pass

@router.get("/estadisticas", summary="R9.4 Estadísticas generales")
def estadisticas(db: Session = Depends(get_db)):
    pass
