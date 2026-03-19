# BiblioUACJ — Sistema de Préstamos de Biblioteca

**Práctica ASD · Métricas del Software · UACJ 2025**

Sistema REST API para gestión de préstamos de biblioteca universitaria.
Construido en Python + FastAPI + SQLite usando la metodología ASD.

---

## ¿Qué es este proyecto?

Cada equipo implementa un módulo independiente del sistema.
Todos los módulos se integran en un solo API funcional al final.

## Estructura

```
biblioUACJ/
├── main.py          # NO modificar — lo mantiene el equipo líder
├── database.py      # NO modificar — modelos compartidos
├── requirements.txt
└── routers/
    ├── libros.py        ← Equipo 1
    ├── usuarios.py      ← Equipo 2
    ├── prestamos.py     ← Equipo 3
    ├── devoluciones.py  ← Equipo 4
    ├── busqueda.py      ← Equipo 5
    ├── historial.py     ← Equipo 6
    ├── multas.py        ← Equipo 7
    ├── inventario.py    ← Equipo 8
    └── reportes.py      ← Equipo 9
```

## Setup rápido

```bash
# 1. Clonar el repo
git clone https://github.com/LuisFlores223046/biblioUACJ.git
cd biblioUACJ

# 2. Cambiarse a tu rama (reemplaza N con tu número de equipo)
git checkout equipo-N

# 3. Crear entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Correr el servidor
uvicorn main:app --reload

# 6. Probar en el navegador
# http://localhost:8000/docs
```

## Reglas importantes

- Cada equipo **solo modifica su archivo** en `routers/`
- **No tocar** `main.py`, `database.py` ni archivos de otros equipos
- Probar cada endpoint en `/docs` antes de hacer commit
- Hacer commit y push al terminar cada endpoint:

```bash
git add routers/tuarchivo.py
git commit -m "feat: implementar endpoint nombre_endpoint"
git push origin equipo-N
```

## ¿No tienes Git o no funciona?

Descarga el ZIP directamente:
**Code → Download ZIP** en esta página

---

*Equipo Líder: Luis Flores, Evelyn Bravo, Rogelio Saucedo · UACJ 2026*
