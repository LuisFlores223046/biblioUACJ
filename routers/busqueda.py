from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Libro, Usuario, Prestamo

# Se crea el router que agrupa los endpoints del módulo de búsqueda
router = APIRouter()

# R5.1 Buscar por título (búsqueda parcial)
@router.get("/titulo/{titulo}", summary="R5.1 Buscar por título")
def buscar_titulo(titulo: str, db: Session = Depends(get_db)):
    """
    Permite buscar libros cuyo título contenga el texto proporcionado.

    Parámetros:
    - titulo: cadena de texto a buscar dentro del campo 'titulo'.
    - db: sesión de base de datos inyectada automáticamente.

    Retorna:
    - Lista de libros que coinciden parcialmente con el título.

    Excepciones:
    - HTTP 404 si no se encuentran resultados.
    """
    # Se realiza una consulta filtrando por coincidencias parciales en el título (sin distinguir mayúsculas/minúsculas)
    resultados = db.query(Libro).filter(Libro.titulo.ilike(f"%{titulo}%")).all()

    # Si no hay resultados, se lanza una excepción
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron libros con ese título")

    return resultados


# R5.2 Buscar por autor
@router.get("/autor/{autor}", summary="R5.2 Buscar por autor")
def buscar_autor(autor: str, db: Session = Depends(get_db)):
    """
    Permite buscar libros cuyo autor contenga el texto proporcionado.

    Parámetros:
    - autor: cadena de texto a buscar dentro del campo 'autor'.
    - db: sesión de base de datos.

    Retorna:
    - Lista de libros que coinciden parcialmente con el autor.

    Excepciones:
    - HTTP 404 si no se encuentran resultados.
    """
    resultados = db.query(Libro).filter(Libro.autor.ilike(f"%{autor}%")).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron libros de ese autor")

    return resultados


# R5.3 Libros disponibles
@router.get("/disponibles", summary="R5.3 Libros disponibles")
def libros_disponibles(db: Session = Depends(get_db)):
    """
    Permite obtener únicamente los libros que se encuentran disponibles.

    Parámetros:
    - db: sesión de base de datos.

    Retorna:
    - Lista de libros disponibles (campo disponible = 1).

    Excepciones:
    - HTTP 404 si no hay libros disponibles.
    """
    # Se filtra por libros disponibles (1 = disponible)
    resultados = db.query(Libro).filter(Libro.disponible == 1).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No hay libros disponibles")

    return resultados


# R5.4 Buscar por ISBN exacto
@router.get("/isbn/{isbn}", summary="R5.4 Buscar por ISBN")
def buscar_isbn(isbn: str, db: Session = Depends(get_db)):
    """
    Permite buscar un libro mediante su ISBN exacto.

    Parámetros:
    - isbn: identificador único del libro.
    - db: sesión de base de datos.

    Retorna:
    - Un objeto libro que coincide con el ISBN.

    Excepciones:
    - HTTP 404 si el libro no existe.
    """
    # Se busca el libro por coincidencia exacta de ISBN
    libro = db.query(Libro).filter(Libro.isbn == isbn).first()

    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return 
    
    # R5.5 Búsqueda general
@router.get("/general/{texto}", summary="R5.5 Búsqueda general")
def busqueda_general(texto: str, db: Session = Depends(get_db)):
    """
    Busca libros por título, autor o ISBN usando un solo parámetro.
    """

    resultados = db.query(Libro).filter(
        (Libro.titulo.ilike(f"%{texto}%")) |
        (Libro.autor.ilike(f"%{texto}%")) |
        (Libro.isbn.ilike(f"%{texto}%"))
    ).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron resultados")

    return resultados

    # R5.6 Libros disponibles por autor
@router.get("/autor-disponibles/{autor}", summary="R5.6 Libros disponibles de un autor")
def autor_disponibles(autor: str, db: Session = Depends(get_db)):
    """
    Lista los libros disponibles de un autor específico.
    """

    resultados = db.query(Libro).filter(
        Libro.autor.ilike(f"%{autor}%"),
        Libro.disponible == 1
    ).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No hay libros disponibles de ese autor")

    return resultados

    # R5.7 Libros prestados con usuario
@router.get("/prestados", summary="R5.7 Libros prestados actualmente")
def libros_prestados(db: Session = Depends(get_db)):
    """
    Lista los libros prestados actualmente mostrando el nombre del usuario.
    """

    prestamos = db.query(Prestamo, Libro, Usuario).join(
        Libro, Prestamo.libro_id == Libro.id
    ).join(
        Usuario, Prestamo.usuario_id == Usuario.id
    ).filter(
        Prestamo.devuelto == False
    ).all()

    resultado = []

    for prestamo, libro, usuario in prestamos:
        resultado.append({
            "libro_id": libro.id,
            "titulo": libro.titulo,
            "usuario": usuario.nombre
        })

    return resultado

    # R5.8 Libros que ha pedido un usuario
@router.get("/usuario/{usuario_id}", summary="R5.8 Libros por usuario")
def libros_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Regresa todos los libros que un usuario ha pedido prestados.
    """

    prestamos = db.query(Prestamo, Libro).join(
        Libro, Prestamo.libro_id == Libro.id
    ).filter(
        Prestamo.usuario_id == usuario_id
    ).all()

    resultado = []

    for prestamo, libro in prestamos:
        resultado.append({
            "libro_id": libro.id,
            "titulo": libro.titulo
        })

    if not resultado:
        raise HTTPException(status_code=404, detail="El usuario no tiene préstamos")

    return resultado
    