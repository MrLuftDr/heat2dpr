import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def cargar_json(ruta: Path) -> dict:
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo de resultados: {ruta}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera grafica comparativa Heat2D")
    parser.add_argument(
        "--serial",
        type=Path,
        default=Path("resultados/v0_serial.json"),
        help="Ruta al JSON de v0_serial",
    )
    parser.add_argument(
        "--prange",
        type=Path,
        default=Path("resultados/v1_prange.json"),
        help="Ruta al JSON de v1_prange",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("resultados/comparativa_heat2d.png"),
        help="Ruta de salida de la imagen PNG",
    )
    args = parser.parse_args()

    datos_v0 = cargar_json(args.serial)
    datos_v1 = cargar_json(args.prange)

    med_v0 = float(datos_v0["mediana_segundos"])
    med_v1 = float(datos_v1["mediana_segundos"])
    speedup = med_v0 / med_v1 if med_v1 > 0 else 0.0

    params = datos_v0.get("parametros", {})
    nx = params.get("nx", 160)
    ny = params.get("ny", 160)
    pasos = params.get("pasos", 120)
    reps = params.get("repeticiones", 5)

    etiquetas = ["v0_serial", "v1_prange"]
    medianas = [med_v0, med_v1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
    fig.suptitle(
        f"Heat2D ({nx}x{ny}, {pasos} pasos, {reps} reps) — Speedup v1_prange: {speedup:.2f}x",
        fontsize=11,
        fontweight="bold",
    )

    barras = ax1.bar(etiquetas, medianas, color=["#5c6b73", "#2a9d8f"], width=0.5)
    ax1.set_title("Mediana de tiempo de ejecucion")
    ax1.set_ylabel("Tiempo (segundos)")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    for barra, valor in zip(barras, medianas):
        ax1.text(
            barra.get_x() + barra.get_width() / 2,
            valor,
            f"{valor:.4f} s",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    reps_idx = list(range(1, len(datos_v0["tiempos_segundos"]) + 1))
    ax2.plot(reps_idx, datos_v0["tiempos_segundos"], marker="o", label="v0_serial", color="#5c6b73")
    ax2.plot(reps_idx, datos_v1["tiempos_segundos"], marker="s", label="v1_prange", color="#2a9d8f")
    ax2.set_title("Tiempo por repeticion (sin warmup)")
    ax2.set_xlabel("Repeticion")
    ax2.set_ylabel("Tiempo (segundos)")
    ax2.set_xticks(reps_idx)
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend()

    plt.tight_layout()
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.salida, dpi=200)
    print(f"Grafica guardada en: {args.salida} | Speedup: {speedup:.2f}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
