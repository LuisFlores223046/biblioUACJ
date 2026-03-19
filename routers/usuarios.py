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
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    pass

@router.get("/", summary="R2.2 Listar usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    pass

@router.get("/{matricula}", summary="R2.3 Buscar por matrícula")
def obtener_usuario(matricula: str, db: Session = Depends(get_db)):
    pass

@router.put("/{usuario_id}/estado", summary="R2.4 Activar/desactivar")
def cambiar_estado(usuario_id: int, activo: bool, db: Session = Depends(get_db)):
    pass

@router.delete("/{usuario_id}", summary="R2.5 Eliminar usuario")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    pass
