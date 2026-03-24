from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from database import get_db, Prestamo, Libro

# Si existen esquemas en schemas.py, impórtalos; si no, define los básicos aquí
from pydantic import BaseModel
from typing import List

class DevolucionResponse(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: date
    fecha_devolucion: date | None
    devuelto: bool
    multa: int | None

    class Config:
        from_attributes = True

router = APIRouter(prefix="/devoluciones", tags=["Devoluciones"])

@router.get("/", response_model=List[DevolucionResponse])
def listar_devoluciones(db: Session = Depends(get_db)):
    """Lista todos los préstamos que ya fueron devueltos."""
    devueltos = db.query(Prestamo).filter(Prestamo.devuelto == True).all()
    return devueltos

@router.get("/{id}", response_model=DevolucionResponse)
def obtener_devolucion(id: int, db: Session = Depends(get_db)):
    """Obtiene una devolución específica por ID."""
    prestamo = db.query(Prestamo).filter(Prestamo.id == id, Prestamo.devuelto == True).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    return prestamo

@router.post("/", response_model=DevolucionResponse)
def registrar_devolucion(prestamo_id: int, db: Session = Depends(get_db)):
    """Registra la devolución de un libro a partir del ID del préstamo."""
    # 1. Buscar el préstamo
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if prestamo.devuelto:
        raise HTTPException(status_code=400, detail="Este préstamo ya fue devuelto")

    # 2. Obtener el libro
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # 3. Marcar devolución
    prestamo.devuelto = True
    prestamo.fecha_devolucion = date.today()
    libro.disponible += 1

    # 4. Calcular multa si aplica (suponiendo préstamo de 7 días)
    fecha_limite = prestamo.fecha_prestamo + timedelta(days=7)
    if date.today() > fecha_limite:
        dias_retraso = (date.today() - fecha_limite).days
        multa = dias_retraso * 10  # $10 por día
        prestamo.multa = multa
    else:
        prestamo.multa = 0

    # 5. Guardar cambios
    db.commit()
    db.refresh(prestamo)

    return prestamo
