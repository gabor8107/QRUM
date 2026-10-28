# QRUM – Optical Atomic-Clock Test (QRUM-C1)

**Research programme:** Quantum Resonance Unified Model (QRUM)  
**Author:** P. Gabor, Independent Researcher, Hungary  
**Accompanying manuscript:** *QRUM Optical Atomic-Clock Test: Differential Searches for Weak Frequency-Dependent Residuals*, Version 2.3 (Scientific Revision, 27 October 2026)  
**Repository:** https://github.com/gabor8107/QRUM  
**Location:** `atomic_clock_test/`

## What this module does

This is the reproducible **QRUM-C1 conditional synthetic benchmark** accompanying the QRUM optical atomic-clock v2.3 preprint. It simulates three **fictional** optical-clock signals, forms two clock-frequency ratios with a shared clock, and recovers an injected sinusoidal fractional variation through covariance-aware generalized least squares (GLS). It estimates a fixed-frequency, 1% empirical false-positive threshold using 2,000 synthetic null trials and tests signal recovery in 1,000 independent synthetic injections.

**Important scope statement:** The simulation does not use measured optical-clock data, demonstrate a new physical interaction, or verify the QRUM hypothesis. The oscillating fine-structure-constant perturbation and its amplitude are *conditional test assumptions*. The synthetic `K` values are not the sensitivity coefficients of any real atomic species. The simplifying response assumption `H(f) = 1` is not an experimentally validated instrument response. A 1% synthetic false-positive threshold is **not** a 95% confidence upper limit on any real physical effect.

## Files

| File | Purpose |
| --- | --- |
| `QRUM_OpticalClock_Synthetic_Benchmark_v2.2.py` | Original unmodified simulation used in the v2.3 manuscript |
| `requirements.txt` | Minimal Python dependency |
| `tests/test_benchmark.py` | Deterministic regression and internal-consistency checks |
| `EXPECTED_OUTPUT.txt` | Console output from the validated reference run |
| `VALIDATION.md` | Comparison with the v2.3 manuscript and limitations |

## Install and reproduce

Prerequisites: Python 3.10+ and NumPy. Run the following commands **from inside `atomic_clock_test/`**.

```bash
python -m pip install -r requirements.txt
python QRUM_OpticalClock_Synthetic_Benchmark_v2.2.py
python -m unittest discover -s tests -v
```

On Windows with the Python launcher you can use `py -3` instead of `python`.

The script is deterministic at the recorded seed (`20261027`); minor variations may occur with changes to the numerical environment. Typical reference output:

```text
Input frequency = 0.010 Hz, N = 10000, dt = 1.0 s
Synthetic response differences = 0.5, 1.5
Predicted ideal output amplitudes = 1.000e-17, 3.000e-17
Injected g = 2.000e-17, fitted g = 2.060e-17, fitted phase = 0.7010 rad
Simulated 1% false-positive threshold (single fixed frequency) = 3.869e-18
Simulated detection probability at injected g = 1.000
```

This is a single fixed-frequency trial at **0.010 Hz**. It does not transfer the 145–155 Hz gravitational-wave analysis window of QBES to clocks.

## Model and test design

The v2.3 preprint posits the optional QRUM-C1 benchmark

```text
δ ln(α_EM)(t) = g cos(2π f0 t + φ)
y_ij,signal(t) = (K_i,α - K_j,α) g cos(2π f0 t + φ)
```

This is a **conditional response prediction** derived from the stated assumption, not a fundamental QRUM-derived coupling law. The synthetic parameter choices are:

| Parameter | Value |
| --- | --- |
| `f0` | 0.010 Hz (100-s period) |
| `g_injected` | 2 × 10^-17 (dimensionless, assumed) |
| `phase` | 0.6 rad |
| Synthetic `K` vector | [1.5, 1.0, 0.0] |
| Ratio differences | ΔK12 = 0.5, ΔK13 = 1.5 |
| Time samples | N = 10,000, Δt = 1 s |
| Individual clock noise | σ = 1 × 10^-16 per sample, independent Gaussian |
| Shared clock | Clock 1 belongs to both ratios; hence nonzero covariance |
| Transfer function | H12 = H13 = 1 (simulation-only assumption) |
| Null simulations | 2,000 |
| Injected simulations | 1,000 |
| Nominal fixed-frequency false-positive probability | 1% |

From the assumed signed response coefficients, the two ideal *amplitude magnitudes* are `1e-17` and `3e-17`, i.e. a 3:1 ratio. For real experiments, independently validated clock transition sensitivities, time stamps, instrument responses, correlated noise, systematics and controls are necessary. Broad-band searches must correct for look-elsewhere effects.

## Connection to the QRUM programme

- **Phase 1 / QBES:** Gravitational-wave residual strain spectra, with its own statistic and bands.
- **QRUM-C1 / Optical clocks:** Fractional-frequency-ratio time series, independently defined statistic and response.

These are complementary research workstreams, **not** the same physical observable, and sharing the QRUM research programme identity does not create a demonstrated cross-instrument coupling.

## DOI and historical releases

The *v2.3 optical-clock manuscript* should be archived on Zenodo and OSF, with a DOI recorded **after it is assigned**. Replace the following text in this README after publication:

`Optical-clock v2.3 Zenodo DOI: PENDING PUBLICATION`

Historical QBES archive (different workstream): https://doi.org/10.5281/zenodo.23602635

The unmodified simulation retains `v2.2` in its filename because the **v2.3** paper explicitly cites that script version. This repository folder is intended to be uploaded alongside the existing `phase-1qbes/` folder; it must not overwrite or replace it.

## Citation

Gabor, P. (2026). *QRUM Optical Atomic-Clock Test: Differential Searches for Weak Frequency-Dependent Residuals*. Version 2.3, Scientific Revision. DOI: pending Zenodo publication.
