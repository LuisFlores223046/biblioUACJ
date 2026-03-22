# Datos de Prueba — BiblioUACJ

La base de datos ya viene cargada con datos reales para que puedas probar tu módulo desde el minuto 1.

## Libros disponibles (IDs 1-10)

| ID | Título | Autor | Disponible |
|----|--------|-------|------------|
| 1  | Ingeniería del Software | Pressman | ❌ Prestado |
| 2  | Clean Code | Robert C. Martin | ❌ Prestado |
| 3  | Algoritmos y Estructuras de Datos | Cormen | ❌ Prestado |
| 4  | El Programador Pragmático | Hunt | ❌ Prestado |
| 5  | Patrones de Diseño | Gang of Four | ❌ Prestado |
| 6  | Fundamentos de Bases de Datos | Silberschatz | ❌ Prestado |
| 7  | Redes de Computadoras | Tanenbaum | ✅ Disponible |
| 8  | Sistemas Operativos Modernos | Tanenbaum | ✅ Disponible |
| 9  | Inteligencia Artificial | Russell | ✅ Disponible |
| 10 | Cálculo Diferencial e Integral | Stewart | ✅ Disponible |

## Usuarios registrados (IDs 1-8)

| ID | Nombre | Matrícula | Activo |
|----|--------|-----------|--------|
| 1  | Ana García López | 223001 | ✅ |
| 2  | Carlos Mendoza Ruiz | 223002 | ✅ |
| 3  | María Torres Vega | 223003 | ✅ |
| 4  | José Hernández Cruz | 223004 | ✅ |
| 5  | Laura Sánchez Díaz | 223005 | ✅ |
| 6  | Miguel Flores Ramos | 223046 | ✅ |
| 7  | Sofía Ramírez Luna | 223007 | ✅ |
| 8  | Diego Castro Mora | 223008 | ❌ Inactivo |

## Préstamos activos (IDs 1-6)

| ID | Libro | Usuario | Días prestado | Vencido? |
|----|-------|---------|---------------|----------|
| 1  | id=1  | id=1    | 3 días | No |
| 2  | id=2  | id=2    | 5 días | No |
| 3  | id=3  | id=3    | 2 días | No |
| 4  | id=5  | id=4    | 1 día  | No |
| 5  | id=4  | id=5    | 12 días | **SÍ — multa pendiente** |
| 6  | id=6  | id=6    | 10 días | **SÍ — multa pendiente** |

## Préstamos devueltos (IDs 7-10)
Historial disponible para los módulos de Historial y Reportes.

## IDs útiles por módulo

- **E3 Préstamos**: Para crear préstamo usa libro_id=7,8,9 o 10 (disponibles) y usuario_id=1-7
- **E4 Devoluciones**: Devuelve préstamos activos con id=1,2,3,4,5,6
- **E5 Búsqueda**: Busca "Software", "Datos", "Tanenbaum"
- **E6 Historial**: usuario_id=1,2,3 tienen historial completo
- **E7 Multas**: préstamo_id=5 y 6 están vencidos (+7 días) — calcular multa
- **E8 Inventario**: libros 7,8,9,10 disponibles; 1-6 prestados
- **E9 Reportes**: Hay 10 préstamos totales con historial variado
