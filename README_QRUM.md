# QRUM — Frequency-Dependent Matter–Curvature Coupling

**Reproducible Python reference implementation** accompanying the manuscript:

> **Einstein–Quantum Resonance Unified Model (QRUM): A Phenomenological Formulation and Exploratory Gravitational-Wave Residual Study**  
> P. Gabor (Independent Researcher)  
> DOI: [10.5281/zenodo.17579967](https://doi.org/10.5281/zenodo.17579967)

---

## What this repository is

This package provides a transparent, fully open reference workflow for exploratory residual-spectrum analysis of gravitational-wave strain data. It implements:

- HDF5 / NumPy strain loading  
- optional simple template subtraction  
- Welch power spectral density estimation  
- frequency-domain whitening  
- instrumental-line exclusion  
- Lorentzian residual fitting  
- AIC / AICc / BIC model comparison  
- bootstrap uncertainty estimation  
- automatic figure and CSV export  

The code does **not** hard-code any numerical results from the manuscript. All parameters are estimated from the supplied data and configuration files.

---

## Scientific scope and limitations

This is a **reference implementation**, not a production-grade LIGO analysis pipeline.

- Exact event-level reproduction of the manuscript results requires the precise detector, GPS interval, strain product, waveform template, PSD estimation settings, filtering choices, fit range, line mask, likelihood definition and priors.
- Without an aligned numerical-relativity template, the pipeline performs a **detector-spectrum analysis** rather than a true post-template residual analysis.
- The included synthetic demonstration deliberately injects a 150 Hz Lorentzian component for educational purposes. It is **not** a claim of detection.

The manuscript itself reports **null / inconclusive** results regarding any astrophysical resonance near 150 Hz. This repository exists to make the analysis method fully reproducible and open to independent scrutiny.

---

## Installation

```bash
python -m venv .venv
```

**Linux / macOS**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Quick start (synthetic demonstration)

```bash
python make_demo_data.py
python run_analysis.py --config config/demo.yaml
```

This will create:
- `results/demo_qrum_summary.json`
- `results/demo_qrum_spectrum.csv`
- `figures/demo_qrum_spectrum_fit.png`
- `figures/demo_qrum_time_series.png`

---

## Real data analysis

1. Place a GWOSC-style `.hdf5` or `.h5` file in the `data/` directory.
2. Edit `config/example_event.yaml` (strain path, start time, duration, optional template, fit range, line mask).
3. Run:

```bash
python run_analysis.py --config config/example_event.yaml
```

---

## Phenomenological model

The effective frequency-dependent factor used in the manuscript is:

```text
f_φ(f) = 1 + α / [1 + ((f − f₀)/(f₀/Q))²]
```

The residual-spectrum test function fitted by the code is:

```text
P(f) = baseline(f) + A / [1 + ((f − f₀)/(f₀/Q))²]
```

where `baseline(f)` is a linear (or optionally other) continuum model.

---

## Model comparison

The package reports residual sum of squares, AIC, AICc, BIC, ΔAICc and ΔBIC.  
These are **exploratory information-criterion diagnostics**, not fully specified Bayesian evidence (Bayes factors). A rigorous Bayesian model comparison would require explicit priors, a properly defined likelihood, and marginalisation over the full parameter space.

---

## Repository structure

```text
QRUM/
├── config/               # YAML configuration files
├── data/                 # Place strain files here (not tracked)
├── figures/              # Output plots
├── results/              # Output JSON and CSV
├── src/                  # Core analysis modules
├── tests/                # Basic unit tests
├── make_demo_data.py     # Synthetic data generator
├── run_analysis.py       # Main entry point
├── requirements.txt
├── LICENSE               # MIT
└── CITATION.cff
```

---

## Citation

If you use this code or the accompanying manuscript, please cite:

- The Zenodo manuscript (DOI: 10.5281/zenodo.17579967)
- This software repository

See `CITATION.cff` for machine-readable citation metadata.

---

## License

- **Code**: MIT License  
- **Manuscript**: Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)

---

## Author

**P. Gabor**  
Independent Researcher  
Contact: p.gabor8107@gmail.com
