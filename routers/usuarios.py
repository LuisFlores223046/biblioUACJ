"""
EQUIPO 2 — Módulo: Gestión de Usuarios
Requerimientos:
  R2.1 Registrar un usuario (nombre, matricula, email)
  R2.2 Consultar todos los usuarios
  R2.3 Consultar usuario por matrícula
  R2.4 Activar / desactivar usuario
  R2.5 Eliminar usuario
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Usuario

router = APIRouter()

class UsuarioCreate(BaseModel):
    nombre: str
    matricula: str
    email: str

# TODO Equipo 2: Implementar los endpoints ↓

@router.post("/", summary="R2.1 Registrar usuario")
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificamos si la matrícula ya existe para evitar duplicados
    existe = db.query(Usuario).filter(Usuario.matricula == datos.matricula).first()
    if existe:
        raise HTTPException(status_code=400, detail="La matrícula ya está registrada")
    
    # Creamos la instancia del modelo
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        matricula=datos.matricula,
        email=datos.email,
        activo=True  # Por defecto entran como activos
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", summary="R2.2 Listar usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    # Consultamos todos los registros de la tabla Usuario
    usuarios = db.query(Usuario).all()
    return usuarios

@router.get("/{matricula}", summary="R2.3 Buscar por matrícula")
def buscar_por_matricula(matricula: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.matricula == matricula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}/estado", summary="R2.4 Activar/desactivar")
def cambiar_estado_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Cambiamos el valor de True a False o viceversa
    usuario.activo = not usuario.activo
    db.commit()
    db.refresh(usuario)
    return {"mensaje": f"Estado del usuario {usuario.nombre} actualizado", "activo": usuario.activo}

@router.delete("/{usuario_id}", summary="R2.5 Eliminar usuario")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}