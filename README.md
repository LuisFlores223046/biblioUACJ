# BiblioUACJ — Sistema de Préstamos de Biblioteca

**Práctica ASD · Métricas del Software · UACJ 2025**

Sistema REST API para gestión de préstamos de biblioteca universitaria, construido con Python + FastAPI + SQLite usando la metodología **Adaptive Software Development (ASD)**.

---

## ¿Qué es este proyecto?

Cada equipo implementa un módulo independiente del sistema. Todos los módulos se integran al final en un solo API funcional demostrable en `/docs`.

La base de datos ya viene con datos de prueba cargados — no necesitas configurar nada.

---

## Requisitos

- Python 3.8 o superior
- Git (opcional — puedes descargar el ZIP si no tienes Git)

---

## Setup rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/LuisFlores223046/biblioUACJ.git
cd biblioUACJ

# 2. Cambiarte a tu rama (reemplaza N con tu número de equipo: 1 al 9)
git checkout equipo-N

# 3. Crear entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Mac / Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Correr el servidor
uvicorn main:app --reload

# 6. Abrir la interfaz de pruebas en el navegador
# http://localhost:8000/docs
```

> **Sin Git:** Descarga el ZIP desde el botón verde **Code → Download ZIP**, descomprime y sigue desde el paso 3.

---

## Estructura del proyecto

```
biblioUACJ/
├── main.py               ← NO modificar — lo mantiene el equipo líder
├── database.py           ← NO modificar — modelos y conexión compartidos
├── requirements.txt      ← dependencias
├── bibliouacj.db         ← base de datos con datos de prueba ya cargados
├── DATOS_DE_PRUEBA.md    ← qué IDs usar para probar tu módulo
└── routers/
    ├── libros.py         ← Equipo 1
    ├── usuarios.py       ← Equipo 2
    ├── prestamos.py      ← Equipo 3
    ├── devoluciones.py   ← Equipo 4
    ├── busqueda.py       ← Equipo 5
    ├── historial.py      ← Equipo 6
    ├── multas.py         ← Equipo 7
    ├── inventario.py     ← Equipo 8
    └── reportes.py       ← Equipo 9
```

---

## Módulos por equipo

| Equipo | Archivo | Módulo | Requerimientos |
|--------|---------|--------|----------------|
| E1 | routers/libros.py | Gestión de Libros | R1.1 al R1.5 |
| E2 | routers/usuarios.py | Gestión de Usuarios | R2.1 al R2.5 |
| E3 | routers/prestamos.py | Registro de Préstamos | R3.1 al R3.4 |
| E4 | routers/devoluciones.py | Devoluciones | R4.1 al R4.4 |
| E5 | routers/busqueda.py | Búsqueda de Libros | R5.1 al R5.4 |
| E6 | routers/historial.py | Historial de Préstamos | R6.1 al R6.3 |
| E7 | routers/multas.py | Control de Multas | R7.1 al R7.4 |
| E8 | routers/inventario.py | Inventario y Disponibilidad | R8.1 al R8.4 |
| E9 | routers/reportes.py | Reportes y Estadísticas | R9.1 al R9.4 |

---

## Base de datos — Datos de prueba disponibles

La BD ya contiene datos reales para que puedas probar desde el minuto 1:

| Tabla | Contenido |
|-------|-----------|
| `libros` | 10 libros. IDs 7, 8, 9 y 10 disponibles. IDs 1–6 ya prestados. |
| `usuarios` | 8 usuarios. IDs 1–7 activos. ID 8 inactivo. |
| `prestamos` | 10 préstamos. 6 activos (IDs 1–6). 4 devueltos (IDs 7–10). Préstamos 5 y 6 están vencidos (+7 días). |

Consulta `DATOS_DE_PRUEBA.md` para ver exactamente qué IDs usar en tu módulo.

---

## Reglas importantes

- Cada equipo **solo modifica su archivo** en `routers/`
- **No tocar** `main.py`, `database.py` ni archivos de otros equipos
- Probar cada endpoint en `/docs` antes de hacer commit
- **No ejecutar DELETE masivos** — afecta las pruebas de todos

---

## Cómo probar tu módulo

1. Corre el servidor: `uvicorn main:app --reload`
2. Abre `http://localhost:8000/docs`
3. Busca tu módulo en la lista
4. Haz clic en un endpoint → **Try it out** → llena los datos → **Execute**
5. Revisa la respuesta en **Response body**

---

## Guardar y subir cambios

```bash
# Cuando un endpoint funcione correctamente:
git add routers/tuarchivo.py
git commit -m "feat: implementar endpoint nombre_del_endpoint"
git push origin equipo-N
```

---

## Problemas comunes

| Problema | Solución |
|----------|----------|
| `python` no se reconoce | Usa `python3` |
| `(venv)` no aparece | Cierra y reabre la terminal, activa el entorno de nuevo |
| `git push` rechazado | Ejecuta `git pull origin equipo-N` primero |
| Servidor se cae al guardar | Error de sintaxis — lee el mensaje en la terminal |
| Error 422 en /docs | Los datos enviados no tienen el formato correcto |
| `Address already in use` | Usa `uvicorn main:app --reload --port 8001` |

---

## Tecnología

- **Python 3** + **FastAPI** — framework del API
- **SQLAlchemy** — ORM para la base de datos
- **SQLite** — base de datos local (no requiere instalación)
- **Pydantic** — validación de datos
- **Uvicorn** — servidor ASGI

---

*Equipo Líder: Luis Flores · Métricas del Software · UACJ 2025*
