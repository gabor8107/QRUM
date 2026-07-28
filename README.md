# QRUM Correlation Framework

**Reproducible multi-sensor correlation analysis** for public gravitational-wave strain data.

Accompanying manuscript:  
**QRUM: A Correlation-Based Framework for Multi-Sensor Analysis of Gravitational-Wave Data**  
Version 1.1 — Scientific Revision (July 2026)  
P. Gabor (Independent Researcher)

---

## Scope

This repository implements a transparent reference pipeline for:

- Loading public GWOSC strain
- Normalization, preprocessing and whitening
- Detector time-alignment via cross-correlation
- Optional simple template subtraction
- Residual spectral analysis
- Lorentzian test-function fitting
- AIC / AICc / BIC comparison
- Bootstrap uncertainty estimation
- Event vs. control comparison

The code does **not** hard-code any manuscript results. All parameters are estimated from the supplied data and configuration.

## Scientific limitation

This is a reference implementation, not a production LIGO analysis pipeline. Exact event-level reproduction requires the precise GPS interval, strain product, template, PSD settings, line mask and priors. Without an aligned numerical-relativity template the pipeline performs a detector-spectrum analysis rather than a true post-template residual analysis.

The manuscript reports **null / inconclusive** results regarding any astrophysical residual resonance. This repository exists to make the method fully reproducible and open to independent scrutiny.

## Mathematical core (as defined in the manuscript)

- Normalized detector signals:  
  `s_i(t) = (S_i(t) − μ_i) / σ_i`

- Cross-correlation and optimal delay:  
  `C(τ) = Σ [H(t) · L(t+τ)] / √(Σ H² · Σ L²)`  
  `Δt = arg max |C(τ)|`

- Residual:  
  `R(t) = H_f(t) − L_aligned(t)`

- Lorentzian test function:  
  `P(f) = baseline(f) + A / [1 + ((f − f₀)/(f₀/Q))²]`

- Optional network quantities (covariance, dominant eigenvalue, coherence index) are defined in the manuscript for future multi-detector extensions.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Quick test (synthetic)

```bash
python make_demo_data.py
python run_analysis.py --config config/demo.yaml
```

## Real data

1. Place GWOSC-style `.hdf5` or `.npy` files in `data/`.
2. Edit `config/example_event.yaml`.
3. Run:

```bash
python run_analysis.py --config config/example_event.yaml
```

## Outputs

- `results/*_summary.json`
- `results/*_spectrum.csv`
- `figures/*_spectrum_fit.png`
- `figures/*_time_series.png`

## License

- **Code**: MIT License  
- **Manuscript**: CC BY-NC-ND 4.0

## Author

P. Gabor  
p.gabor8107@gmail.com
