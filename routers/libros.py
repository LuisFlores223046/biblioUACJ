"""
EQUIPO 1 — Módulo: Gestión de Libros
Requerimientos:
  R1.1 Registrar un libro (titulo, autor, isbn, cantidad)
  R1.2 Consultar todos los libros
  R1.3 Consultar un libro por ID
  R1.4 Actualizar datos de un libro
  R1.5 Eliminar un libro
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Libro

router = APIRouter()

class LibroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    cantidad: int = 1

# TODO Equipo 1: Implementar los endpoints ↓

@router.post("/", summary="R1.1 Registrar libro", status_code=status.HTTP_201_CREATED)
def crear_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    """
    registrmos un nuevo libro 
    nos aseguramos de que no existan libros con el mismo ISBN que es su id
    si existe lanzamos un error 400
    y si no existe lo creamos
    """
    existente = db.query(Libro).filter(Libro.isbn == libro.isbn).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un libro con ese ISBN")

    nuevo_libro = Libro(
        titulo=libro.titulo,
        autor=libro.autor,
        isbn=libro.isbn,
        cantidad=libro.cantidad,
    )
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)

    return {
        "id": nuevo_libro.id,
        "titulo": nuevo_libro.titulo,
        "autor": nuevo_libro.autor,
        "isbn": nuevo_libro.isbn,
        "cantidad": nuevo_libro.cantidad,
        "disponible": nuevo_libro.disponible,
    }


@router.get("/", summary="R1.2 Listar todos los libros")
def listar_libros(db: Session = Depends(get_db)):
    """
    retornamos todos los libros que existen en la base de datos
    """
    return db.query(Libro).all()

@router.get("/{libro_id}", summary="R1.3 Consultar libro por ID")
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    """
    **Consultar un libro específico por su identificador único.**

    - **libro_id**: El ID numérico del libro almacenado en la base de datos.
    - **Retorna**: Los detalles del libro si existe, de lo contrario lanza un error 404.
    """
    libro_db = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return libro_db

@router.put("/{libro_id}", summary="R1.4 Actualizar libro")
def actualizar_libro(libro_id: int, libro: LibroCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un libro por su ID.

    - `libro_id`: identificador del libro a actualizar.
    - `libro`: nuevo contenido del libro.
    """
    libro_db = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro_db.titulo = libro.titulo
    libro_db.autor = libro.autor
    libro_db.isbn = libro.isbn
    libro_db.cantidad = libro.cantidad
    libro_db.disponible = libro.cantidad > 0

    db.commit()
    db.refresh(libro_db)

    return {
        "mensaje": "Libro actualizado correctamente",
        "libro": {
            "id": libro_db.id,
            "titulo": libro_db.titulo,
            "autor": libro_db.autor,
            "isbn": libro_db.isbn,
            "cantidad": libro_db.cantidad,
            "disponible": libro_db.disponible,
        },
    }

@router.delete("/{libro_id}", summary="R1.5 Eliminar libro")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    """
    **Eliminar un libro de la base de datos de forma permanente.**

    - **libro_id**: El ID del libro que se desea borrar.
    - **Validación**: Si el ID no existe, se retorna un error 404.
    - **Resultado**: Confirmación de la eliminación exitosa.
    """
    libro_db = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro_db)
    db.commit()

    return {"mensaje": "Libro eliminado correctamente", "libro_id": libro_id}
