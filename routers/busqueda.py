from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Libro

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

    return libro