"""
Simple spectrum plotting (no Lorentzian overlay).
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_spectrum(
    f: np.ndarray,
    p: np.ndarray,
    outfile: Path,
    title: str = "Residual spectrum",
    target_band: tuple | None = None,
) -> None:
    """Plot residual spectrum; optionally shade a fixed target band."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.semilogy(f, p, lw=0.8, color="0.2", label="residual power")

    if target_band is not None:
        ax.axvspan(target_band[0], target_band[1], color="C0", alpha=0.15, label="target band")

    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Power spectral density")
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    fig.tight_layout()
    outfile.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outfile, dpi=150)
    plt.close(fig)
