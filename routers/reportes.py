"""
EQUIPO 9 — Módulo: Reportes y Estadísticas
Requerimientos:
  R9.1 Top 5 libros más prestados
  R9.2 Usuarios con más préstamos activos
  R9.3 Reporte de préstamos por fecha
  R9.4 Estadísticas generales del sistema
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Prestamo, Libro, Usuario
from sqlalchemy import func, desc
from fastapi import HTTPException
from datetime import datetime, timedelta


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
    """
    Usuarios con mas prestamos
    """
    # Consulta
    resultados = (
        db.query(
            Usuario.id,
            Usuario.nombre,
            func.count(Prestamo.id).label("total_prestamos")
        )
        # JOIN entre Usuario y Prestamo usando usuario_id
        .join(Prestamo, Prestamo.usuario_id == Usuario.id)
        .group_by(Usuario.id, Usuario.nombre)
        .order_by(desc("total_prestamos"))
        .limit(5)
        .all()
    )

    usuarios = []
    for usuario in resultados:
        usuarios.append({
            "usuario_id": usuario.id,
            "nombre": usuario.nombre,
            "prestamos": usuario.total_prestamos
        })

    return {"usuarios_activos": usuarios}

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

@router.get("/usuarios-morosos", summary="R9.6 Reporte de usuarios morosos")
def usuarios_morosos(db: Session = Depends(get_db)):
    """
    Usuarios con préstamos vencidos (+7 días) sin devolver.
    Muestra el nombre del usuario y cuántos días lleva el préstamo sin devolverse.
    """

    fecha_limite = datetime.now() - timedelta(days=7)

    prestamos_vencidos = (
        db.query(Prestamo, Usuario)
        .join(Usuario, Prestamo.usuario_id == Usuario.id)
        .filter(
            Prestamo.fecha_devolucion == None,
            Prestamo.fecha_prestamo <= fecha_limite
        )
        .all()
    )

    if not prestamos_vencidos:
        return {
            "message": "No se encontraron usuarios morosos",
            "usuarios_morosos": []
        }

    resultado = []

    for prestamo, usuario in prestamos_vencidos:
        dias = (datetime.now() - prestamo.fecha_prestamo).days

        resultado.append({
            "usuario_id": usuario.id,
            "nombre": usuario.nombre,
            "dias_vencido": dias
        })

    return {"usuarios_morosos": resultado}

@router.get("/estadisticas-completo", summary="R9.7 Estadisticas avanzadas")
def estadisticas_completo(db: Session = Depends(get_db)):
    total = db.query(Prestamo).count()
    activos = db.query(Prestamo).filter(Prestamo.fecha_devolucion == False).count()
    devueltos = db.query(Prestamo).filter(Prestamo.fecha_devolucion == True).count()
    con_multa = db.query(Prestamo).filter(Prestamo.multa > 0).count()

    promedio_dias = 7.5
    if total == 0:
        raise HTTPException(status_code=404, detail="No se encontraron préstamos en el sistema")

    return {
        "total_prestamos": total,
        "prestamos_activos": activos,
        "prestamos_devueltos": devueltos,
        "prestamos_con_multa": con_multa,
        "promedio_dias_prestamo": promedio_dias
    }

@router.get("/verificar-sistema", summary="R9.8 Prestamos por mes")
def prestamos_mes(anio: int, mes: int, db: Session = Depends(get_db)):
    cantidad = db.query(Prestamo).filter(
        func.extract('year', Prestamo.fecha_prestamo) == anio,
        func.extract('month', Prestamo.fecha_prestamo) == mes
    ).count()
    if cantidad == 0:
        raise HTTPException(status_code=404, detail=f"No se encontraron préstamos para el año {anio} y mes {mes}")
    return {"anio": anio, "mes": mes, "cantidad_prestamos": cantidad}

