#!/usr/bin/env python3
"""
Statistical Survey of Compact Object Frequencies
Basic reproducible pipeline skeleton (KDE + GMM + BIC + bootstrap).

Replace the synthetic example data with the curated tables in data/.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.neighbors import KernelDensity
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")

DATA = Path(__file__).resolve().parents[1] / "data"
OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(exist_ok=True)

def load_example_frequencies():
    """Synthetic placeholder – replace with real curated CSVs."""
    rng = np.random.default_rng(42)
    # pretend log-frequency samples for illustration
    wd = rng.normal(loc=-2.5, scale=0.4, size=200)      # white-dwarf like
    psr = rng.normal(loc=0.2, scale=0.8, size=2000)     # pulsar like
    return {
        "white_dwarfs": wd,
        "pulsars": psr,
    }

def kde_1d(x, bandwidth=None):
    x = np.asarray(x).reshape(-1, 1)
    if bandwidth is None:
        grid = GridSearchCV(KernelDensity(kernel="gaussian"),
                            {"bandwidth": np.logspace(-2, 1, 20)}, cv=5)
        grid.fit(x)
        bandwidth = grid.best_params_["bandwidth"]
    kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth).fit(x)
    return kde, bandwidth

def gmm_bic(x, max_components=8):
    x = np.asarray(x).reshape(-1, 1)
    bics = []
    models = []
    for n in range(1, max_components + 1):
        gm = GaussianMixture(n_components=n, covariance_type="full", random_state=0)
        gm.fit(x)
        bics.append(gm.bic(x))
        models.append(gm)
    best = int(np.argmin(bics)) + 1
    return models[best - 1], best, bics

def bootstrap_peak_recovery(x, n_boot=500, bandwidth=0.3):
    """Very simple peak-location stability check."""
    x = np.asarray(x)
    peaks = []
    rng = np.random.default_rng(0)
    grid = np.linspace(x.min(), x.max(), 512).reshape(-1, 1)
    for _ in range(n_boot):
        sample = rng.choice(x, size=len(x), replace=True).reshape(-1, 1)
        kde = KernelDensity(bandwidth=bandwidth).fit(sample)
        log_dens = kde.score_samples(grid)
        peaks.append(grid[np.argmax(log_dens), 0])
    return np.percentile(peaks, [16, 50, 84])

def main():
    datasets = load_example_frequencies()
    print("=== Compact Object Frequency Survey – pipeline skeleton ===\n")
    for name, freqs in datasets.items():
        print(f"[{name}]  n = {len(freqs)}")
        kde, bw = kde_1d(freqs)
        print(f"  KDE bandwidth: {bw:.4f}")
        gm, n_comp, bics = gmm_bic(freqs)
        print(f"  GMM best components (BIC): {n_comp}")
        q16, q50, q84 = bootstrap_peak_recovery(freqs, bandwidth=max(bw, 0.1))
        print(f"  Bootstrap peak (16/50/84%): {q16:.3f} / {q50:.3f} / {q84:.3f}\n")
    print("Replace load_example_frequencies() with real curated tables from data/.")
    print("Full analysis scripts and notebooks can be added under src/ and notebooks/.")

if __name__ == "__main__":
    main()
