"""Tests for Lorentzian-free residual utilities (v2.1)."""

import numpy as np
import pytest
from src.model import (
    band_density,
    fixed_band_excess,
    baseline_linear,
    validate_spectrum,
    bootstrap_excess_ratio_windows,
)


def test_validate_increasing():
    f = np.array([1.0, 2.0, 3.0])
    p = np.ones(3)
    validate_spectrum(f, p)  # must not raise


def test_validate_rejects_unsorted():
    f = np.array([1.0, 3.0, 2.0])
    p = np.ones(3)
    with pytest.raises(ValueError, match="strictly increasing"):
        validate_spectrum(f, p)


def test_band_density_flat():
    freqs = np.linspace(100, 200, 1001)
    power = np.ones_like(freqs)
    d = band_density(freqs, power, 145, 155)
    assert abs(d - 1.0) < 0.05


def test_band_density_large_gap_returns_nan():
    freqs = np.linspace(100, 200, 1001)
    power = np.ones_like(freqs)
    # Punch a large hole in the middle of the target band
    power[(freqs >= 147) & (freqs <= 153)] = np.nan
    d = band_density(freqs, power, 145, 155, max_gap_hz=2.0)
    # Usable width is too small → NaN
    assert np.isnan(d)


def test_fixed_band_excess_flat():
    freqs = np.linspace(100, 200, 2001)
    power = np.ones_like(freqs)
    out = fixed_band_excess(freqs, power, 145, 155, 120, 145, 155, 180)
    assert abs(out["excess_ratio"] - 1.0) < 0.05


def test_fixed_band_excess_elevated():
    freqs = np.linspace(100, 200, 2001)
    power = np.ones_like(freqs)
    mask = (freqs >= 145) & (freqs <= 155)
    power[mask] = 2.0
    out = fixed_band_excess(freqs, power, 145, 155, 120, 145, 155, 180)
    assert out["excess_ratio"] > 1.5


def test_baseline_linear():
    f = np.array([1.0, 2.0, 3.0])
    y = baseline_linear(f, 10.0, 2.0)
    assert np.allclose(y, [12.0, 14.0, 16.0])


def test_classify_invalid_not_neutral():
    from run_analysis import classify_ratio
    assert classify_ratio(np.nan) == "invalid"
    assert classify_ratio(1.0) == "null_or_consistent_with_local_background"
    assert classify_ratio(1.5) == "elevated_power_in_target_band"
    assert classify_ratio(0.5) == "deficit_in_target_band"


def test_bootstrap_windows_runs():
    freqs = np.linspace(100, 200, 1001)
    windows = np.stack([np.ones_like(freqs) * v for v in [1, 2, 3, 4]])
    boot = bootstrap_excess_ratio_windows(freqs, windows, 145, 155, 120, 145, 155, 180, n_bootstrap=50, seed=1)
    assert boot["n_windows"] == 4
    assert abs(boot["mean"] - 1) < 1e-10


def test_band_density_partial_coverage_consistent():
    freqs = np.linspace(100, 200, 1001)
    power = np.ones_like(freqs) * 3
    power[(freqs > 149) & (freqs < 150)] = np.nan
    assert abs(band_density(freqs, power, 145, 155) - 3) < 1e-10


def test_band_density_rejects_low_coverage():
    freqs = np.linspace(100, 200, 1001)
    power = np.ones_like(freqs)
    power[(freqs > 147) & (freqs < 153)] = np.nan
    assert np.isnan(band_density(freqs, power, 145, 155))
