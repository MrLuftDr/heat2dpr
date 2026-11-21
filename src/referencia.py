import numpy as np


def crear_malla_referencia(nx: int = 160, ny: int = 160) -> np.ndarray:
    """Malla inicial identica para verificacion de correctitud."""
    u = np.zeros((nx, ny), dtype=np.float64)
    x0, x1 = nx // 4, (3 * nx) // 4
    y0, y1 = ny // 4, (3 * ny) // 4
    u[x0:x1, y0:y1] = 100.0
    return u


def heat2d_referencia(
    u_inicial: np.ndarray,
    pasos: int = 120,
    alpha: float = 0.2,
    dt: float = 1.0,
    dx: float = 1.0,
    dy: float = 1.0,
) -> np.ndarray:
    """Modelo de referencia en float64 con cortes de arreglo (stencil de 5 puntos)."""
    u = np.array(u_inicial, dtype=np.float64, copy=True)
    rx = alpha * dt / (dx * dx)
    ry = alpha * dt / (dy * dy)
    rc = 1.0 - 2.0 * (rx + ry)

    for _ in range(pasos):
        u_next = u.copy()
        u_next[1:-1, 1:-1] = (
            rc * u[1:-1, 1:-1]
            + rx * (u[:-2, 1:-1] + u[2:, 1:-1])
            + ry * (u[1:-1, :-2] + u[1:-1, 2:])
        )
        u = u_next

    return u
