"""
EQUIPO 9 — Módulo: Reportes y Estadísticas
Requerimientos:
  R9.1 Top 5 libros más prestados
  R9.2 Usuarios con más préstamos activos
  R9.3 Reporte de préstamos por fecha
  R9.4 Estadísticas generales del sistema
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from database import get_db, Prestamo, Libro, Usuario

router = APIRouter()

# TODO Equipo 9: Implementar los endpoints ↓

@router.get("/top-libros", summary="R9.1 Top 5 libros más prestados")
def top_libros(db: Session = Depends(get_db)):
    """Recuperar los préstamos agrupados por libro_id y contar las veces que se ha prestado cada libro"""

    #Recuperar todos los préstamos y contar las veces que se ha prestado cada libro
    prestamos = db.query(Prestamo).all()
    veces_prestados = {} 

    for prestamo in prestamos:
        libro_id = prestamo.libro_id
        if libro_id not in veces_prestados:
            veces_prestados[libro_id] = 0  
        veces_prestados[libro_id] += 1 

    #Ordenar de mayor a menor y tomar los primeros 5
    veces_prestados_ordenado = sorted(veces_prestados.items(), key=lambda x: x[1], reverse=True)
    top_5 = veces_prestados_ordenado[:5]
    resultado = []

    #Recuperar los detalles de cada libro del top 5
    for libro_id, total_prestamos in top_5:
        libro = db.query(Libro).filter(Libro.id == libro_id).first()

        if libro:
            resultado.append({"libro_id": libro.id, "titulo": libro.titulo, "autor": libro.autor, 
                              "isbn": libro.isbn,"cantidad": libro.cantidad, "prestamos": total_prestamos})

    return {"top_libros": resultado}

@router.get("/usuarios-activos", summary="R9.2 Usuarios con más préstamos")
def usuarios_activos(db: Session = Depends(get_db)):
    pass

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db, Prestamo, Libro, Usuario
from typing import List

router = APIRouter()

@router.get("/por-fecha", summary="R9.3 Préstamos por fecha")
def prestamos_por_fecha(fecha: str, db: Session = Depends(get_db)):

    try:
        # Filtramos comparando solo la parte de la fecha (date) del campo DateTime
        resultados = db.query(Prestamo).filter(
            func.date(Prestamo.fecha_prestamo) == fecha
        ).all()
        
        if not resultados:
            return {"message": f"No se encontraron préstamos para la fecha {fecha}", "data": []}
            
        return resultados
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

@router.get("/estadisticas", summary="R9.4 Estadísticas generales")
def estadisticas(db: Session = Depends(get_db)):

    # Consultas de Libros
    total_libros = db.query(Libro).count()
    libros_disponibles = db.query(Libro).filter(Libro.disponible == True).count()

    # Consultas de Usuarios
    total_usuarios = db.query(Usuario).count()
    usuarios_activos = db.query(Usuario).filter(Usuario.activo == True).count()

    # Consultas de Préstamos
    total_prestamos = db.query(Prestamo).count()
    prestamos_activos = db.query(Prestamo).filter(Prestamo.devuelto == False).count()

    return {
        "libros": {
            "total": total_libros,
            "disponibles": libros_disponibles,
            "prestados": total_libros - libros_disponibles
        },
        "usuarios": {
            "total": total_usuarios,
            "activos": usuarios_activos,
            "inactivos": total_usuarios - usuarios_activos
        },
        "prestamos": {
            "total_historico": total_prestamos,
            "activos_actualmente": prestamos_activos,
            "finalizados": total_prestamos - prestamos_activos
        }
    }
