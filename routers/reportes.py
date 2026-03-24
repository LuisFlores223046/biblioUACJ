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
