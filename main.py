"""
BiblioUACJ — Sistema de Préstamos de Biblioteca
UACJ · Métricas del Software · 2025

Archivo de integración — mantenido por el EQUIPO LÍDER.
Cada equipo registra su router aquí al terminar su módulo.
"""
from fastapi import FastAPI
from database import create_tables

from routers import libros       # Equipo 1
from routers import usuarios     # Equipo 2
from routers import prestamos    # Equipo 3
from routers import devoluciones # Equipo 4
from routers import busqueda     # Equipo 5
from routers import historial    # Equipo 6
from routers import multas       # Equipo 7
from routers import inventario   # Equipo 8
from routers import reportes     # Equipo 9

app = FastAPI(
    title="BiblioUACJ",
    description="Sistema de Préstamos de Biblioteca · Práctica ASD · UACJ 2025",
    version="1.0.0"
)

create_tables()

app.include_router(libros.router,       prefix="/libros",       tags=["Libros — E1"])
app.include_router(usuarios.router,     prefix="/usuarios",     tags=["Usuarios — E2"])
app.include_router(prestamos.router,    prefix="/prestamos",    tags=["Préstamos — E3"])
app.include_router(devoluciones.router, prefix="/devoluciones", tags=["Devoluciones — E4"])
app.include_router(busqueda.router,     prefix="/busqueda",     tags=["Búsqueda — E5"])
app.include_router(historial.router,    prefix="/historial",    tags=["Historial — E6"])
app.include_router(multas.router,       prefix="/multas",       tags=["Multas — E7"])
app.include_router(inventario.router,   prefix="/inventario",   tags=["Inventario — E8"])
app.include_router(reportes.router,     prefix="/reportes",     tags=["Reportes — E9"])

@app.get("/", tags=["Sistema"])
def root():
    return {
        "sistema": "BiblioUACJ",
        "version": "1.0.0",
        "docs": "Abre /docs para probar todos los endpoints",
        "modulos": {
            "E1": "/libros", "E2": "/usuarios", "E3": "/prestamos",
            "E4": "/devoluciones", "E5": "/busqueda", "E6": "/historial",
            "E7": "/multas", "E8": "/inventario", "E9": "/reportes"
        }
    }
