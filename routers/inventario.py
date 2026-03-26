"""
EQUIPO 8 — Módulo: Inventario y Disponibilidad
Requerimientos:
  R8.1 Ver inventario completo con disponibilidad
  R8.2 Ver libros con stock bajo (menos de 2 disponibles)
  R8.3 Actualizar cantidad de un libro
  R8.4 Ver resumen del inventario (total libros, disponibles, prestados)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func #Nuevo import
from database import get_db, Libro, Prestamo

router = APIRouter()

# TODO Equipo 8: Implementar los endpoints ↓

@router.get("/", summary="R8.1 Inventario completo")
def inventario_completo(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todos los libros con su información de stock.
 
    Campos relevantes por libro:
    - id, titulo, autor, isbn
    - cantidad   → total de ejemplares que posee la biblioteca
    - disponible → booleano: True si se puede prestar, False si no
    - prestados  → ejemplares actualmente fuera (calculado aquí)
    """
    libros = db.query(Libro).all()
    
    print("LIBROS:", libros)
    print("TOTAL:", len(libros))
    
    resultado = []
    for libro in libros:
        prestamos_activos = (
            db.query(func.count(Prestamo.id))
            .filter(Prestamo.libro_id==libro.id, Prestamo.devuelto==False)
            .scalar()
        )
        resultado.append({
            "id":libro.id,
            "titulo":libro.titulo,
            "autor":libro.autor,
            "isbn":libro.isbn,
            "cantidad":libro.cantidad,
            "disponible":libro.disponible,
            "prestados":prestamos_activos
        })

    return {
        "total_libros": len(resultado),
        "libros": resultado, 
    }

@router.get("/stock-bajo", summary="R8.2 Libros con stock bajo")
def stock_bajo(db: Session = Depends(get_db)):
    """
    Devuelve los libros cuyo numero de ejemplares libres es menor a 2.
 
    Como `disponible` es booleano, no podemos filtrar directamente con < 2.
    En cambio, calculamos: ejemplares_libres = cantidad - prestamos_activos
    y marcamos stock bajo cuando ese valor es 0 o 1.
 
    Estrategia:
      1. Traemos todos los libros (tabla pequena, aceptable).
      2. Para cada libro contamos sus prestamos activos.
      3. Filtramos en Python los que tienen ejemplares_libres < 2.
 
    Alternativa mas eficiente (si la BD crece mucho): subquery con GROUP BY,
    pero para este sistema es innecesario.
    """
    libros = db.query(Libro).all()
 
    resultado = []
    for libro in libros:
        prestamos_activos = (
            db.query(func.count(Prestamo.id))
            .filter(Prestamo.libro_id == libro.id, Prestamo.devuelto == False)
            .scalar()
        )
        ejemplares_libres = libro.cantidad - prestamos_activos
 
        if ejemplares_libres < 2:
            resultado.append({
                "id":               libro.id,
                "titulo":           libro.titulo,
                "autor":            libro.autor,
                "cantidad":         libro.cantidad,
                "disponible":       libro.disponible,       # bool del modelo
                "prestados":        prestamos_activos,
                "ejemplares_libres": ejemplares_libres,
                # Etiqueta para el frontend
                "alerta": "SIN STOCK" if ejemplares_libres == 0 else "STOCK CRITICO",
            })
 
    if not resultado:
        return {
            "mensaje": "Todos los libros tienen stock suficiente.",
            "libros":  [],
        }
 
    return {
        "total_con_stock_bajo": len(resultado),
        "libros": resultado,
    }

@router.put("/{libro_id}/cantidad", summary="R8.3 Actualizar cantidad")
def actualizar_cantidad(libro_id: int, cantidad: int, db: Session = Depends(get_db)):
    """
    Modifica el número total de ejemplares (`cantidad`) de un libro.
 
    Reglas de negocio:
    1. La nueva `cantidad` debe ser >= 1.
    2. La nueva `cantidad` NO puede ser menor que los ejemplares ya prestados,
       porque no puedes eliminar libros que estan fuera de la biblioteca.
    3. El campo `disponible` (bool) se recalcula automaticamente:
         disponible = (cantidad_nueva - prestados_activos) > 0
       True  -> hay al menos un ejemplar libre para prestar
       False -> todos los ejemplares estan prestados
 
    Ejemplo:
      Libro con cantidad=5, prestados=3 -> disponible=True (quedan 2)
      Si actualizas cantidad a 7 -> disponible=True (quedan 4)  OK
      Si actualizas cantidad a 3 -> disponible=False (quedan 0) OK
      Si intentas cantidad=2     -> ERROR (menos que los 3 prestados)  ERROR
    """
    # 1. Buscar el libro; 404 si no existe
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail=f"Libro con id={libro_id} no encontrado.")
 
    # 2. Validar que la nueva cantidad sea positiva
    if cantidad < 1:
        raise HTTPException(
            status_code=400,
            detail="La cantidad debe ser al menos 1."
        )
 
    # 3. Calcular cuantos ejemplares estan prestados actualmente
    prestados_activos = (
        db.query(func.count(Prestamo.id))
        .filter(Prestamo.libro_id == libro_id, Prestamo.devuelto == False)
        .scalar()
    )
 
    # 4. No permitir que la nueva cantidad sea menor que los ya prestados
    if cantidad < prestados_activos:
        raise HTTPException(
            status_code=400,
            detail=(
                f"No se puede reducir la cantidad a {cantidad}. "
                f"Hay {prestados_activos} ejemplar(es) actualmente prestados."
            ),
        )
 
    # 5. Guardar valores anteriores para incluirlos en la respuesta
    cantidad_anterior   = libro.cantidad
    disponible_anterior = libro.disponible  # bool
 
    # 6. Actualizar cantidad y recalcular disponible como booleano.
    #    disponible = True si queda al menos 1 ejemplar libre tras el cambio.
    libro.cantidad = cantidad
    libro.disponible = (cantidad - prestados_activos) > 0  # True o False
 
    db.commit()
    db.refresh(libro)
 
    return {
        "mensaje":  f"Cantidad del libro '{libro.titulo}' actualizada correctamente.",
        "libro_id": libro.id,
        "titulo":   libro.titulo,
        "antes": {
            "cantidad":   cantidad_anterior,
            "disponible": disponible_anterior,
        },
        "despues": {
            "cantidad":          libro.cantidad,
            "disponible":        libro.disponible,          # bool actualizado
            "ejemplares_libres": libro.cantidad - prestados_activos,
        },
        "prestados_activos": prestados_activos,
    }
    

@router.get("/resumen", summary="R8.4 Resumen del inventario")
def resumen_inventario(db: Session = Depends(get_db)):
    """
    Devuelve metricas agregadas de todo el inventario.
 
    Metricas incluidas:
    - total_titulos        -> cuantos libros distintos hay en el catalogo
    - total_ejemplares     -> suma de `cantidad` de todos los libros
    - libros_disponibles   -> cuantos titulos tienen disponible=True
    - libros_no_disponibles-> cuantos titulos tienen disponible=False
    - total_prestados      -> prestamos activos contados desde la tabla Prestamo
    - total_ejemplares_libres -> total_ejemplares - total_prestados
 
    Nota: `disponible` es booleano, por eso usamos count con filtro en lugar
    de sum. No tiene sentido sumar True/False como si fueran numeros.
    """
    # Total de titulos y suma de ejemplares fisicos
    total_titulos = db.query(func.count(Libro.id)).scalar()
    total_ejemplares = db.query(func.sum(Libro.cantidad)).scalar() or 0
    
    # Libros disponibles / no disponibles (filtrando por el bool)
    libros_disponibles = (
        db.query(func.count(Libro.id)).filter(Libro.disponible == True).scalar()
    )
    libros_no_disponibles = (
        db.query(func.count(Libro.id)).filter(Libro.disponible == False).scalar()
    )
    
    # Prestamos activos: fuente de verdad para saber cuantos ejemplares están fuera
    total_prestados = (
        db.query(func.count(Prestamo.id))
        .filter(Prestamo.devuelto == False)
        .scalar()
    )
    
    return {
        "Total_titulos":total_titulos,
        "Total_ejemplares":total_ejemplares,
        "libros_disponibles":libros_disponibles, # titulos con disponible=True
        "libros_no_disponibles":libros_no_disponibles, # titulos con disponible=False
        "total_prestados":total_prestados, # prestamos activos
        "total_ejemplares_libres":total_ejemplares-total_prestados, # en estante
    }


# ─── NUEVOS ENDPOINTS ITERACIÓN 2 ────────────────────────────────────────────

@router.get("/disponibilidad-real", summary="R8.5 Disponibilidad real por libro")
def disponibilidad_real(db: Session = Depends(get_db)):
    """
    Calcula la disponibilidad real de cada libro (cantidad total menos préstamos activos).
    """
    try:
        libros = db.query(Libro).all()
        resultado = []
        for libro in libros:
            prestamos_activos = db.query(func.count(Prestamo.id)).filter(
                Prestamo.libro_id == libro.id,
                Prestamo.devuelto == False
            ).scalar() or 0
            
            disponibilidad = libro.cantidad - prestamos_activos
            
            resultado.append({
                "libro_id": libro.id,
                "titulo": libro.titulo,
                "cantidad_total": libro.cantidad,
                "prestamos_activos": prestamos_activos,
                "disponibilidad_real": disponibilidad
            })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular disponibilidad: {str(e)}")

@router.get("/estado-critico", summary="R8.6 Libros en estado crítico")
def libros_estado_critico(db: Session = Depends(get_db)):
    """
    Lista los libros cuya disponibilidad real es menor o igual a 1.
    """
    try:
        libros = db.query(Libro).all()
        resultado = []
        for libro in libros:
            prestamos_activos = db.query(func.count(Prestamo.id)).filter(
                Prestamo.libro_id == libro.id,
                Prestamo.devuelto == False
            ).scalar() or 0
            
            disponibilidad = libro.cantidad - prestamos_activos
            
            if disponibilidad <= 1:
                resultado.append({
                    "libro_id": libro.id,
                    "titulo": libro.titulo,
                    "cantidad_total": libro.cantidad,
                    "prestamos_activos": prestamos_activos,
                    "disponibilidad_real": disponibilidad
                })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estado crítico: {str(e)}")

@router.get("/extremos", summary="R8.7 Libro más y menos prestado")
def extremos_prestamos(db: Session = Depends(get_db)):
    """
    Regresa el libro que más se ha prestado y el que menos se ha prestado en la historia.
    """
    try:
        estadisticas = db.query(
            Libro.id, 
            Libro.titulo, 
            func.count(Prestamo.id).label('total_prestamos')
        ).outerjoin(Prestamo).group_by(Libro.id).all()

        if not estadisticas:
            raise HTTPException(status_code=404, detail="No hay datos suficientes en el inventario.")

        estadisticas_ordenadas = sorted(estadisticas, key=lambda x: x.total_prestamos)
        
        menos_prestado = estadisticas_ordenadas[0]
        mas_prestado = estadisticas_ordenadas[-1]

        return {
            "mas_prestado": {
                "libro_id": mas_prestado.id,
                "titulo": mas_prestado.titulo,
                "total_veces_prestado": mas_prestado.total_prestamos
            },
            "menos_prestado": {
                "libro_id": menos_prestado.id,
                "titulo": menos_prestado.titulo,
                "total_veces_prestado": menos_prestado.total_prestamos
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular extremos: {str(e)}")

@router.get("/ocupacion", summary="R8.8 Resumen de ocupación")
def resumen_ocupacion(db: Session = Depends(get_db)):
    """
    Devuelve un resumen con el total de libros, ejemplares, préstamos actuales y porcentaje de ocupación.
    """
    try:
        total_libros = db.query(func.count(Libro.id)).scalar() or 0
        ejemplares_totales = db.query(func.sum(Libro.cantidad)).scalar() or 0
        
        prestados_actualmente = db.query(func.count(Prestamo.id)).filter(
            Prestamo.devuelto == False
        ).scalar() or 0
        
        porcentaje_ocupacion = 0.0
        if ejemplares_totales > 0:
            porcentaje_ocupacion = (prestados_actualmente / ejemplares_totales) * 100

        return {
            "total_libros_distintos": total_libros,
            "ejemplares_totales": ejemplares_totales,
            "prestados_actualmente": prestados_actualmente,
            "porcentaje_ocupacion": round(porcentaje_ocupacion, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el reporte de ocupación: {str(e)}")