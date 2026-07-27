# QRUM — Frequency-Dependent Matter–Curvature Coupling

Reproducible Python reference implementation accompanying the manuscript:

**Einstein–Quantum Resonance Unified Model (QRUM): A Phenomenological Formulation and Exploratory Gravitational-Wave Residual Study**

Author: P. Gabor  
DOI: `10.5281/zenodo.17579967`

## Scope

This repository implements a transparent reference workflow for:

- HDF5 strain loading
- optional template subtraction
- Welch power spectral density estimation
- frequency-domain whitening
- instrumental-line exclusion
- Lorentzian residual fitting
- AIC/AICc/BIC model comparison
- bootstrap uncertainty estimation
- figure and CSV export

The code does **not** hard-code the manuscript's reported fit values. It estimates parameters from the supplied data and configuration.

## Scientific limitation

Exact event-level reproduction requires the precise detector, GPS interval, strain product, waveform/template, PSD segment, filtering choices, fit range, line mask, likelihood and priors. This package therefore provides a reference pipeline and a fully reproducible synthetic demonstration.

Without an aligned waveform template, the program performs a detector-spectrum analysis rather than a true post-template residual analysis.

## Installation

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick test

```bash
python make_demo_data.py
python run_analysis.py --config config/demo.yaml
```

## Real data

1. Put a GWOSC-style `.hdf5` or `.h5` file in `data/`.
2. Edit `config/example_event.yaml`.
3. Run:

```bash
python run_analysis.py --config config/example_event.yaml
```

## Main model

```text
f_phi(f) = 1 + alpha / [1 + ((f - f0)/(f0/Q))^2]
```

Residual-spectrum test function:

```text
P(f) = baseline(f) + amplitude / [1 + ((f - f0)/(f0/Q))^2]
```

## Outputs

- `results/*_summary.json`
- `results/*_spectrum.csv`
- `figures/*_spectrum_fit.png`
- `figures/*_time_series.png`

## Model comparison

The package reports RSS, AIC, AICc, BIC, Delta AICc and Delta BIC. These are exploratory diagnostics, not a fully specified Bayes factor.

## License

Code: MIT License. The manuscript may remain under its separately stated CC BY-NC-ND 4.0 license.
