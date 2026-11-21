# Heat2D — Difusion Termica 2D (HPC)

Proyecto final de Computacion de Alto Desempeno (UTP, 2026-2): simulacion de difusion termica en una malla bidimensional (`400x400`, `200` pasos temporales) mediante diferencias finitas explicitas (stencil de 5 puntos), comparando la linea base serial (`src/v0_serial.py`) frente a la implementacion paralela en memoria compartida con Numba `prange` (`src/v1_prange.py`).

## Integrantes y roles
- **Sebastian Bello** y **Alejandro Arenas** (roles de implementador y medidor alternados durante el proyecto).

## Estructura del proyecto
```text
heat2dpr/
├── README.md             # Descripcion e instrucciones de reproduccion
├── pyproject.toml        # Dependencias y version fijada de Python (3.12)
├── reproducir.sh         # Comando unico para verificar, medir y graficar
├── generar_grafica.py    # Genera grafica comparativa desde resultados/*.json
├── src/
│   ├── __init__.py
│   ├── referencia.py     # Modelo de referencia para verificacion numerica
│   ├── v0_serial.py      # Linea base serial en Python
│   └── v1_prange.py      # Version paralela con Numba (@njit + prange)
├── test_correctitud.py   # Validacion PASS/FAIL contra referencia.py (tol = 1e-6)
├── bench.py              # Benchmark con 5 repeticiones, mediana y metadatos
└── resultados/           # Archivos JSON y grafica PNG generados por cada corrida


## Instalacion y reproduccion
Desde la carpeta del proyecto:

```bash
uv sync
bash reproducir.sh

#Repositorio en GITHUB

```Repositorio
https://github.com/MrLuftDr/heat2dpr
