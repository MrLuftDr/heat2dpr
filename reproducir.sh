#!/usr/bin/env bash
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$RAIZ"

mkdir -p resultados

echo "[1/4] Verificando correctitud contra referencia.py (400x400, 200 pasos)..."
uv run python test_correctitud.py

echo "[2/4] Midiendo linea base v0_serial (5 repeticiones, 400x400, 200 pasos)..."
uv run python bench.py --version v0_serial --repeticiones 5 --nx 400 --ny 400 --pasos 200 --salida resultados/v0_serial.json

echo "[3/4] Midiendo version paralela v1_prange (5 repeticiones, 400x400, 200 pasos, con warmup JIT)..."
uv run python bench.py --version v1_prange --repeticiones 5 --nx 400 --ny 400 --pasos 200 --salida resultados/v1_prange.json

echo "[4/4] Generando grafica comparativa..."
uv run python generar_grafica.py --serial resultados/v0_serial.json --prange resultados/v1_prange.json --salida resultados/comparativa_heat2d.png

echo "Listo. Resultados y grafica guardados en: $RAIZ/resultados/"
