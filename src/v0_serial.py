import numpy as np


def crear_malla_inicial(nx: int = 160, ny: int = 160) -> np.ndarray:
    """Crea la malla inicial 2D con bordes a 0.0 y un bloque central caliente."""
    u = np.zeros((nx, ny), dtype=np.float64)
    x0, x1 = nx // 4, (3 * nx) // 4
    y0, y1 = ny // 4, (3 * ny) // 4
    u[x0:x1, y0:y1] = 100.0
    return u


def heat2d_serial(
    u_inicial: np.ndarray,
    pasos: int = 120,
    alpha: float = 0.2,
    dt: float = 1.0,
    dx: float = 1.0,
    dy: float = 1.0,
) -> np.ndarray:
    """Difusion termica 2D explicita (stencil de 5 puntos) en Python serial."""
    u = np.array(u_inicial, dtype=np.float64, copy=True)
    nx, ny = u.shape
    rx = alpha * dt / (dx * dx)
    ry = alpha * dt / (dy * dy)
    rc = 1.0 - 2.0 * (rx + ry)

    for _ in range(pasos):
        u_next = u.copy()
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                u_next[i, j] = (
                    rc * u[i, j]
                    + rx * (u[i - 1, j] + u[i + 1, j])
                    + ry * (u[i, j - 1] + u[i, j + 1])
                )
        u = u_next

    return u


if __name__ == "__main__":
    malla = crear_malla_inicial(160, 160)
    resultado = heat2d_serial(malla, pasos=120)
    print("Forma:", resultado.shape, "| Suma final:", float(resultado.sum()))
