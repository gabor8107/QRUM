# QRUM Phase 1 — Frequency-Domain Residual Framework

**Version 2.2 – Lorentzian-free, coverage-consistent**

Reproducible residual-analysis pipeline for public gravitational-wave strain spectra.

---

## What changed in v2.1

- Frequency grid must be strictly increasing (validated on input).
- Masked gaps larger than `max_gap_hz` are not bridged by the integrator.
- Invalid (NaN) excess ratio is classified as `invalid`, never as `neutral`.
- Linear baseline fit is **diagnostic only** and does **not** modify the excess ratio.
- No invalid bin-wise bootstrap. Optional bootstrap of the mean QBES across independent off-source PSD windows only.
- Clearer documentation of scope and limits.

Still completely free of Lorentzian profiles and free peak-frequency parameters.

---

## Scope and hard limits

This repository does **not**:

- propose a generally covariant gravitational action;
- modify the Einstein field equations;
- claim detection of new physics;
- fit any parametric peak profile (Lorentzian or otherwise).

The linear baseline is reported only as a diagnostic.  
The scientific quantity of interest is the **parameter-free fixed-band excess ratio**.

---

## Fixed-band excess ratio

```text
excess_ratio = (density in target band) / average(density in left band, density in right band)
```

Default bands (configurable in YAML):

| Band    | Range        |
|---------|--------------|
| Target  | 145–155 Hz   |
| Left    | 120–145 Hz   |
| Right   | 155–180 Hz   |

Interpretation flag (descriptive only):

| Condition          | Flag                                          |
|--------------------|-----------------------------------------------|
| ratio is NaN       | `invalid`                                     |
| ratio > 1.25       | `elevated_power_in_target_band`               |
| ratio < 0.80       | `deficit_in_target_band`                      |
| otherwise          | `null_or_consistent_with_local_background`    |

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick test

```bash
python make_demo_data.py
PYTHONPATH=. python run_analysis.py --config config/demo.yaml
PYTHONPATH=. python tests/test_model.py
```

## Configuration notes

- `max_gap_hz` (default 2.0): maximum allowed frequency gap inside a band after masking. Larger gaps cause the band density to return NaN if coverage falls below 50%.
- `n_bootstrap` / `seed`: apply only if `data.offsource_spectra` lists at least three independent PSD CSV files on the same frequency grid.
- A single spectrum does **not** produce a confidence interval. Off-source bootstrap intervals describe the off-source *mean*, not on-source detection significance.
- Band density always divides by actually covered frequency width; coverage below 80% returns NaN.
- Off-source CSVs must use the same column names and frequency grid as the primary spectrum.
- The baseline fit never enters the excess-ratio calculation.

## Outputs

- `results/*_summary.json` — excess ratio, optional off-source window-mean bootstrap, diagnostic baseline, interpretation flag
- `results/*_spectrum.csv`
- `figures/*_spectrum.png`

## License

- **Code**: MIT License

## Author

P. Gabor — Independent Researcher

## v2.2 audit notes

- Fixed band integration now splits all gaps larger than `max_gap_hz` and uses one consistent observed-width denominator. Minimum coverage is 80% for every band.
- Removed the former whole-spectrum shuffled-bin bootstrap: it erased frequency structure and did not provide a valid confidence interval.
- Optional `data.offsource_spectra` is a YAML list of **independent** off-source spectrum CSV paths; each is processed identically. Bootstrap estimates only the uncertainty of the mean off-source QBES.
- No p-value, astrophysical detection claim, or on-source confidence interval is supplied.
- The repository accepts precomputed spectral CSVs and does not reproduce raw GWOSC strain preprocessing.
- Fixed-band boundaries are prespecified for this protocol, but can be configured; do not optimize them on the same data and then treat them as preregistered.
