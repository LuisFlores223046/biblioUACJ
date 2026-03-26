from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from database import get_db, Usuario, Prestamo # Importamos Prestamo para la Iteración 2

router = APIRouter()

# Esquema para creación de usuarios
class UsuarioCreate(BaseModel):
    nombre: str
    matricula: str
    email: str

# --- ITERACIÓN 1: 

@router.post("/", summary="R2.1 Registrar usuario")
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario validando que la matrícula sea única."""
    existe = db.query(Usuario).filter(Usuario.matricula == datos.matricula).first()
    if existe:
        raise HTTPException(status_code=400, detail="La matrícula ya está registrada")
    
    nuevo_usuario = Usuario(**datos.dict(), activo=True)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", summary="R2.2 Listar todos los usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    """Retorna la lista completa de usuarios en el sistema."""
    return db.query(Usuario).all()

@router.get("/buscar/{matricula}", summary="R2.3 Buscar por matrícula")
def buscar_por_matricula(matricula: str, db: Session = Depends(get_db)):
    """Busca un usuario específico usando su número de matrícula."""
    usuario = db.query(Usuario).filter(Usuario.matricula == matricula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}/estado", summary="R2.4 Activar/desactivar")
def cambiar_estado_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Cambia el estado de activo a inactivo y viceversa."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.activo = not usuario.activo
    db.commit()
    db.refresh(usuario)
    return {"mensaje": f"Estado de {usuario.nombre} actualizado", "activo": usuario.activo}

@router.delete("/{usuario_id}", summary="R2.5 Eliminar usuario")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Elimina permanentemente un usuario de la base de datos."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}


# --- ITERACIÓN 2

@router.get("/reporte/con-prestamos", summary="R2.6 Usuarios con préstamos activos")
def usuarios_con_prestamos_activos(db: Session = Depends(get_db)):
    """Lista usuarios que tienen al menos un libro en su poder actualmente."""
    return db.query(Usuario).join(Prestamo).filter(Prestamo.devuelto == False).distinct().all()

@router.get("/reporte/sin-historial", summary="R2.7 Usuarios que nunca han pedido libros")
def usuarios_sin_historial(db: Session = Depends(get_db)):
    """Lista usuarios que no registran ningún préstamo en el sistema."""
    prestamos_ids = db.query(Prestamo.usuario_id).distinct().subquery()
    return db.query(Usuario).filter(Usuario.id.notin_(prestamos_ids)).all()

@router.get("/{usuario_id}/resumen", summary="R2.8 Resumen de actividad")
def resumen_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Muestra el conteo de libros activos y devueltos por ID de usuario."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    activos = db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id, Prestamo.devuelto == False).count()
    devueltos = db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id, Prestamo.devuelto == True).count()
    
    return {"nombre": usuario.nombre, "activos": activos, "devueltos": devueltos}

@router.get("/reporte/morosos", summary="R2.9 Usuarios con préstamos vencidos")
def usuarios_morosos(db: Session = Depends(get_db)):
    """Lista usuarios con préstamos de más de 7 días sin devolver."""
    return db.query(Usuario).join(Prestamo).filter(
        Prestamo.devuelto == False, 
        Prestamo.dias_prestamo > 7
    ).distinct().all()

@router.get("/reporte/top-lector", summary="R2.10 Usuario con más préstamos")
def usuario_top(db: Session = Depends(get_db)):
    """Identifica al usuario con mayor cantidad de préstamos totales."""
    res = db.query(Usuario, func.count(Prestamo.id)).join(Prestamo).group_by(Usuario.id).order_by(func.count(Prestamo.id).desc()).first()
    if not res:
        return {"error": "No hay datos"}
    return {"usuario": res[0].nombre, "total_prestamos": res[1]}
 