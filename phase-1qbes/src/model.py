"""
Spectral utilities for residual analysis.

No Lorentzian profile.
No free peak frequency.
No resonance model.
"""

from __future__ import annotations

import numpy as np


def validate_spectrum(freqs: np.ndarray, power: np.ndarray) -> None:
    """Raise if frequency grid is invalid."""
    freqs = np.asarray(freqs, dtype=float)
    power = np.asarray(power, dtype=float)
    if freqs.ndim != 1 or power.ndim != 1:
        raise ValueError("freqs and power must be 1-D arrays")
    if len(freqs) != len(power):
        raise ValueError("freqs and power must have the same length")
    if len(freqs) < 2:
        raise ValueError("need at least 2 frequency points")
    if not np.all(np.isfinite(freqs)):
        raise ValueError("freqs contain non-finite values")
    # Strictly increasing
    df = np.diff(freqs)
    if not np.all(df > 0):
        raise ValueError("frequency grid must be strictly increasing")


def baseline_linear(f: np.ndarray, a: float, b: float) -> np.ndarray:
    """Simple linear baseline in frequency domain (diagnostic only)."""
    return a + b * f


def band_density(
    freqs: np.ndarray,
    power: np.ndarray,
    fmin: float,
    fmax: float,
    max_gap_hz: float = 2.0,
    min_coverage: float = 0.80,
) -> float:
    """Mean PSD over *observed* frequency coverage, never across masked gaps.

    Each connected segment is integrated separately. All cases use the same
    observed-width denominator. Insufficient coverage returns NaN rather than
    silently treating masked frequencies as zero power.
    """
    freqs = np.asarray(freqs, dtype=float)
    power = np.asarray(power, dtype=float)
    if not (np.isfinite(fmin) and np.isfinite(fmax) and fmax > fmin):
        raise ValueError("invalid frequency band")
    if not (np.isfinite(max_gap_hz) and max_gap_hz > 0):
        raise ValueError("max_gap_hz must be positive")
    if not (0 < min_coverage <= 1):
        raise ValueError("min_coverage must be in (0, 1]")
    validate_spectrum(freqs, power)
    mask = (freqs >= fmin) & (freqs <= fmax) & np.isfinite(power) & (power >= 0)
    if np.count_nonzero(mask) < 2:
        return np.nan
    f, v = freqs[mask], power[mask]
    cuts = np.where(np.diff(f) > max_gap_hz)[0] + 1
    total_area = 0.0
    observed_width = 0.0
    for fs, ps in zip(np.split(f, cuts), np.split(v, cuts)):
        if len(fs) >= 2:
            total_area += float(np.trapezoid(ps, fs))
            observed_width += float(fs[-1] - fs[0])
    nominal_width = float(fmax - fmin)
    if observed_width <= 0 or observed_width / nominal_width < min_coverage:
        return np.nan
    return total_area / observed_width


def fixed_band_excess(
    freqs: np.ndarray,
    power: np.ndarray,
    target_low: float,
    target_high: float,
    left_low: float,
    left_high: float,
    right_low: float,
    right_high: float,
    max_gap_hz: float = 2.0,
) -> dict:
    """
    Parameter-free excess statistic in a pre-defined target band
    relative to the average of two neighbouring bands.
    """
    validate_spectrum(freqs, power)

    eq = band_density(freqs, power, target_low, target_high, max_gap_hz)
    el = band_density(freqs, power, left_low, left_high, max_gap_hz)
    er = band_density(freqs, power, right_low, right_high, max_gap_hz)
    bg = 0.5 * (el + er)

    ratio = np.nan
    if np.isfinite(bg) and bg > 0 and np.isfinite(eq):
        ratio = float(eq / bg)

    return {
        "target_density": eq,
        "left_density": el,
        "right_density": er,
        "background_density": bg,
        "excess_ratio": ratio,
    }


def bootstrap_excess_ratio_windows(
    freqs: np.ndarray,
    window_powers: np.ndarray,
    target_low: float, target_high: float,
    left_low: float, left_high: float,
    right_low: float, right_high: float,
    n_bootstrap: int = 500,
    seed: int = 42,
    max_gap_hz: float = 2.0,
) -> dict:
    """Bootstrap independent off-source *windows*, never individual FFT bins.

    Each row must be a PSD from a separate, comparably processed time window.
    The percentile interval describes the mean QBES of those windows, NOT the
    uncertainty or significance of a separate on-source QBES measurement.
    """
    windows = np.asarray(window_powers, dtype=float)
    validate_spectrum(freqs, windows[0] if windows.ndim == 2 and len(windows) else np.array([]))
    if windows.ndim != 2 or windows.shape[1] != len(freqs):
        raise ValueError("window_powers must be a 2-D array matching freqs")
    if len(windows) < 3:
        raise ValueError("at least 3 independent off-source windows are required")
    if n_bootstrap < 20:
        raise ValueError("n_bootstrap must be >= 20")
    values = []
    for row in windows:
        out = fixed_band_excess(freqs, row, target_low, target_high,
                                left_low, left_high, right_low, right_high,
                                max_gap_hz)
        values.append(out["excess_ratio"])
    values = np.asarray(values)
    if not np.all(np.isfinite(values)):
        raise ValueError("all off-source windows must have valid QBES values")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(values), size=(n_bootstrap, len(values)))
    means = values[indices].mean(axis=1)
    return {
        "method": "independent_off_source_window_bootstrap",
        "scope": "uncertainty_of_mean_off_source_QBES_not_on_source_significance",
        "n_windows": int(len(values)),
        "n_valid": int(n_bootstrap),
        "mean": float(means.mean()),
        "std": float(means.std(ddof=1)),
        "ci_16": float(np.percentile(means, 16)),
        "ci_84": float(np.percentile(means, 84)),
    }
