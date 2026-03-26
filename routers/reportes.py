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
from sqlalchemy import func
from fastapi import HTTPException

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
    """Recuperar el total de libros, usuarios y préstamos, y separar préstamos activos y devueltos para 
    generar un resumen general del sistema"""

    #Recuperar el total de libros, usuarios y préstamos
    libros = db.query(Libro).all()
    total_libros = len(libros)
    usuarios = db.query(Usuario).all()
    total_usuarios = len(usuarios)
    prestamos = db.query(Prestamo).all()
    total_prestamos = len(prestamos)
    prestamos_activos = 0
    prestamos_devueltos = 0

    #Separar préstamos activos y devueltos
    for prestamo in prestamos:
        if prestamo.fecha_devolucion is None:  
            prestamos_activos += 1
        else:
            prestamos_devueltos += 1

    #Devolver resumen general del sistema
    return {
        "total_libros": total_libros,
        "total_usuarios": total_usuarios,
        "total_prestamos": total_prestamos,
        "prestamos_activos": prestamos_activos,
        "prestamos_devueltos": prestamos_devueltos
    }

@router.get("/top-libros-mayor-a-menor", summary="R9.5 Top 5 libros más prestados con título, autor y número de préstamos, ordenado de mayor a menor")
def top_libros_mayor_a_menor(db: Session = Depends(get_db)):
    try:
        resultados = (
            db.query(
                Libro.id.label("libro_id"),
                Libro.titulo,
                Libro.autor,
                func.count(Prestamo.id).label("prestamos")
            )
            .join(Prestamo, Prestamo.libro_id == Libro.id)
            .group_by(Libro.id, Libro.titulo, Libro.autor)
            .order_by(func.count(Prestamo.id).desc())
            .all()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el top de libros: {str(e)}"
        )

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron préstamos registrados."
        )

    top_libros = [
        {
            "libro_id": r.libro_id,
            "titulo": r.titulo,
            "autor": r.autor,
            "prestamos": r.prestamos
        }
        for r in resultados
    ]
    return {"top_libros": top_libros}
