import argparse
import json
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numba
import numpy as np
import psutil

RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.v0_serial import crear_malla_inicial, heat2d_serial
from src.v1_prange import heat2d_prange


def metadatos_maquina() -> dict:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "sistema": platform.system(),
        "release": platform.release(),
        "arquitectura": platform.machine(),
        "procesador": platform.processor(),
        "nucleos_fisicos": psutil.cpu_count(logical=False),
        "nucleos_logicos": psutil.cpu_count(logical=True),
        "ram_total_bytes": psutil.virtual_memory().total,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "numba_version": numba.__version__,
        "numba_threads": numba.get_num_threads(),
    }


def medir_version(version: str, repeticiones: int, nx: int, ny: int, pasos: int) -> dict:
    malla = crear_malla_inicial(nx, ny)
    tiempos = []
    warmup_seg = 0.0

    if version == "v0_serial":
        fn = heat2d_serial
    elif version == "v1_prange":
        fn = heat2d_prange
        t0_w = time.perf_counter()
        _ = fn(malla, pasos=min(5, pasos))
        warmup_seg = time.perf_counter() - t0_w
    else:
        raise ValueError(f"Version desconocida: {version}")

    for _ in range(repeticiones):
        t0 = time.perf_counter()
        _ = fn(malla, pasos=pasos)
        t1 = time.perf_counter()
        tiempos.append(t1 - t0)

    return {
        "version": version,
        "parametros": {"nx": nx, "ny": ny, "pasos": pasos, "repeticiones": repeticiones},
        "warmup_segundos": warmup_seg,
        "tiempos_segundos": tiempos,
        "mediana_segundos": statistics.median(tiempos),
        "minimo_segundos": min(tiempos),
        "maximo_segundos": max(tiempos),
        "maquina": metadatos_maquina(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark Heat2D")
    parser.add_argument("--version", choices=["v0_serial", "v1_prange"], required=True)
    parser.add_argument("--repeticiones", type=int, default=5)
    parser.add_argument("--nx", type=int, default=400)
    parser.add_argument("--ny", type=int, default=400)
    parser.add_argument("--pasos", type=int, default=200)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()

    if args.repeticiones < 5:
        raise ValueError("Se requieren al menos 5 repeticiones segun la rubrica del curso.")

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    registro = medir_version(args.version, args.repeticiones, args.nx, args.ny, args.pasos)
    args.salida.write_text(json.dumps(registro, indent=2), encoding="utf-8")
    print(f"{args.version}: mediana = {registro['mediana_segundos']:.6f} s -> {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
