#!/usr/bin/env python3
"""
QRUM Phase 1 — residual analysis entry point (Lorentzian-free, v2.1).

Performs:
- input validation (strictly increasing frequency grid)
- residual spectrum loading / band selection
- optional line masking (gap-safe integration)
- linear baseline fit (diagnostic only – does NOT modify the excess ratio)
- fixed-band excess ratio (parameter-free)
- simple bootstrap uncertainty on the excess ratio

No Lorentzian.
No free peak frequency.
No resonance model.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.config_io import load_config
from src.masking import apply_line_mask
from src.fitting import fit_linear_baseline, aic_bic
from src.model import (
    baseline_linear,
    fixed_band_excess,
    bootstrap_excess_ratio_windows,
    validate_spectrum,
)
from src.plotting import plot_spectrum


def classify_ratio(ratio: float) -> str:
    """Classify excess ratio. NaN → invalid (never neutral)."""
    if not np.isfinite(ratio):
        return "invalid"
    if ratio > 1.25:
        return "elevated_power_in_target_band"
    if ratio < 0.80:
        return "deficit_in_target_band"
    return "null_or_consistent_with_local_background"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="QRUM Phase 1 residual analysis (no Lorentzian, v2.1)"
    )
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()

    cfg = load_config(args.config)
    pr = cfg.get("project", {})
    d = cfg.get("data", {})
    a = cfg.get("analysis", {})

    stem = pr.get("name", "run").replace(" ", "_")
    Path("results").mkdir(exist_ok=True)
    Path("figures").mkdir(exist_ok=True)

    df = pd.read_csv(d["path"])
    f = df[d["frequency_column"]].values.astype(float)
    p = df[d["power_column"]].values.astype(float)

    # Validate before any processing
    validate_spectrum(f, p)

    m = (f >= a["f_min"]) & (f <= a["f_max"])
    f, p = f[m], p[m]
    validate_spectrum(f, p)

    lines = a.get("mask_lines_Hz", [])
    if lines:
        p = apply_line_mask(f, p, lines, a.get("mask_half_width_Hz", 1.0))

    valid = np.isfinite(p) & (p > 0)
    # Keep frequency grid; masked points become NaN in power
    # For excess we pass the full (f, p) with NaNs – band_density handles them
    f_v = f
    p_v = np.where(valid, p, np.nan)

    n_valid = int(np.count_nonzero(np.isfinite(p_v)))
    print(f"Points in analysis band (finite power): {n_valid}")

    # --- Diagnostic baseline (does NOT enter the excess calculation) ---
    fit = fit_linear_baseline(f[valid], p[valid])
    if fit["success"]:
        yhat = baseline_linear(f[valid], fit["a"], fit["b"])
        aic_b, bic_b = aic_bic(p[valid], yhat, k=2)
        print(f"Baseline fit (diagnostic only): a = {fit['a']:.3e}, b = {fit['b']:.3e}")
    else:
        aic_b, bic_b = np.nan, np.nan
        print("Baseline fit failed:", fit.get("reason"))

    # --- Fixed-band excess (parameter-free, on original residual power) ---
    tb = a.get("target_band", [145.0, 155.0])
    left = a.get("left_band", [120.0, 145.0])
    right = a.get("right_band", [155.0, 180.0])
    max_gap = float(a.get("max_gap_hz", 2.0))

    excess = fixed_band_excess(
        f_v, p_v,
        target_low=tb[0], target_high=tb[1],
        left_low=left[0], left_high=left[1],
        right_low=right[0], right_high=right[1],
        max_gap_hz=max_gap,
    )
    ratio = excess["excess_ratio"]
    flag = classify_ratio(ratio)
    print(f"Fixed-band excess ratio ({tb[0]}–{tb[1]} Hz): {ratio}")
    print(f"Interpretation flag: {flag}")

    # Uncertainty is unavailable for one spectrum. Only independent,
    # comparably processed off-source PSD windows can be bootstrapped.
    boot = None
    offsource_paths = d.get("offsource_spectra", [])
    if offsource_paths:
        windows = []
        for path in offsource_paths:
            other = pd.read_csv(path)
            of = other[d["frequency_column"]].to_numpy(dtype=float)
            op = other[d["power_column"]].to_numpy(dtype=float)
            if of.shape != f.shape or not np.allclose(of, f, rtol=0, atol=1e-9):
                raise ValueError(f"Off-source frequency grid mismatch: {path}")
            if lines:
                op = apply_line_mask(of, op, lines, a.get("mask_half_width_Hz", 1.0))
            windows.append(np.where(np.isfinite(op) & (op > 0), op, np.nan))
        boot = bootstrap_excess_ratio_windows(
            f, np.asarray(windows), tb[0], tb[1], left[0], left[1],
            right[0], right[1], n_bootstrap=int(a.get("n_bootstrap", 500)),
            seed=int(a.get("seed", 42)), max_gap_hz=max_gap,
        )
        print("Off-source window-mean QBES bootstrap:", boot)
    else:
        print("No off-source windows supplied: no bootstrap CI is reported.")

    summary = {
        "project": pr.get("name"),
        "n_points_finite": n_valid,
        "baseline_diagnostic_only": True,
        "baseline_success": bool(fit.get("success")),
        "baseline_a": fit.get("a"),
        "baseline_b": fit.get("b"),
        "AIC_baseline": aic_b,
        "BIC_baseline": bic_b,
        "target_band_Hz": tb,
        "left_band_Hz": left,
        "right_band_Hz": right,
        "max_gap_hz": max_gap,
        "target_density": excess["target_density"],
        "background_density": excess["background_density"],
        "excess_ratio": ratio,
        "offsource_window_mean_bootstrap": boot,
        "interpretation": flag,
        "note": (
            "Parameter-free fixed-band excess ratio. "
            "Linear baseline is diagnostic only and does not modify the excess ratio. "
            "No Lorentzian, no free peak frequency, no detection claim. "
            "No confidence interval is estimated from a single spectrum."
        ),
    }

    with open(Path("results") / f"{stem}_summary.json", "w") as fp:
        json.dump(summary, fp, indent=2)

    pd.DataFrame({
        "frequency_Hz": f_v,
        "power": p_v,
    }).to_csv(Path("results") / f"{stem}_spectrum.csv", index=False)

    plot_spectrum(
        f[valid], p[valid],
        Path("figures") / f"{stem}_spectrum.png",
        title=pr.get("name", "Residual spectrum"),
        target_band=(tb[0], tb[1]),
    )

    print("Done. Results written to results/ and figures/.")


if __name__ == "__main__":
    main()
