import sys
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.referencia import crear_malla_referencia, heat2d_referencia
from src.v0_serial import heat2d_serial
from src.v1_prange import heat2d_prange

TOLERANCIA = 1e-6
NX = 400
NY = 400
PASOS = 200


def verificar_version(nombre: str, fn, malla_inicial: np.ndarray, esperado: np.ndarray) -> bool:
    obtenido = fn(malla_inicial, pasos=PASOS)
    error_max = float(np.max(np.abs(obtenido - esperado)))
    pasa = bool(np.allclose(obtenido, esperado, rtol=TOLERANCIA, atol=TOLERANCIA))
    estado = "PASS" if pasa else "FAIL"
    print(f"[{estado}] {nombre:12s} | error_max = {error_max:.2e} (tol = {TOLERANCIA:.0e})")
    return pasa


def main() -> int:
    malla = crear_malla_referencia(NX, NY)
    esperado = heat2d_referencia(malla, pasos=PASOS)

    ok_v0 = verificar_version("v0_serial", heat2d_serial, malla, esperado)
    _ = heat2d_prange(malla, pasos=2)
    ok_v1 = verificar_version("v1_prange", heat2d_prange, malla, esperado)

    return 0 if (ok_v0 and ok_v1) else 1


if __name__ == "__main__":
    raise SystemExit(main())
