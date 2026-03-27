# BiblioUACJ — Sistema de Préstamos de Biblioteca
Práctica ASD · Métricas del Software · UACJ 2026

---

## Setup

```bash
git clone https://github.com/LuisFlores223046/biblioUACJ.git
cd biblioUACJ
git checkout equipo-N       # reemplaza N con tu número de equipo

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Abrir en el navegador: **http://localhost:8000/docs**

---

## Estructura

```
biblioUACJ/
├── main.py               ← no modificar
├── database.py           ← no modificar
├── requirements.txt
├── bibliouacj.db         ← BD con datos de prueba ya cargados
├── DATOS_DE_PRUEBA.md    ← qué IDs usar para probar
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

## Reglas

- Solo modificar tu archivo en `routers/`
- No tocar `main.py`, `database.py` ni archivos de otros equipos
- Probar cada endpoint en `/docs` antes de hacer commit
- Commit y push al terminar cada endpoint:

```bash
git add routers/tuarchivo.py
git commit -m "feat: implementar endpoint nombre"
git push origin equipo-N
```

- Al terminar todos tus endpoints, abrir un **Pull Request** de `equipo-N` a `main`

---

## Datos de prueba disponibles

| Tabla | Contenido |
|-------|-----------|
| libros | 10 libros. Disponibles: IDs 7, 8, 9, 10. Prestados: IDs 1–6. |
| usuarios | 8 usuarios. Activos: IDs 1–7. Inactivo: ID 8. |
| prestamos | 10 préstamos. Activos: IDs 1–6. Devueltos: IDs 7–10. Vencidos: IDs 5 y 6. |

Ver `DATOS_DE_PRUEBA.md` para detalle completo.

---

*Equipo Líder: Luis Flores, Evelyn Nahomi, Rogelio Saucedo · UACJ 2026*
