import numpy as np
from numba import njit, prange


@njit(parallel=True)
def _paso_prange(u: np.ndarray, u_next: np.ndarray, rc: float, rx: float, ry: float) -> None:
    nx, ny = u.shape
    for i in prange(1, nx - 1):
        for j in range(1, ny - 1):
            u_next[i, j] = (
                rc * u[i, j]
                + rx * (u[i - 1, j] + u[i + 1, j])
                + ry * (u[i, j - 1] + u[i, j + 1])
            )


def heat2d_prange(
    u_inicial: np.ndarray,
    pasos: int = 120,
    alpha: float = 0.2,
    dt: float = 1.0,
    dx: float = 1.0,
    dy: float = 1.0,
) -> np.ndarray:
    """Difusion termica 2D paralela en memoria compartida con Numba prange."""
    u = np.array(u_inicial, dtype=np.float64, copy=True)
    rx = alpha * dt / (dx * dx)
    ry = alpha * dt / (dy * dy)
    rc = 1.0 - 2.0 * (rx + ry)

    for _ in range(pasos):
        u_next = u.copy()
        _paso_prange(u, u_next, rc, rx, ry)
        u = u_next

    return u
