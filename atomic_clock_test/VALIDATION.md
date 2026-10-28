# QRUM-C1 benchmark verification – 28 October 2026

## Verification scope

The supplied manuscript `QRUM_Optical_Atomic_Clock_Test_v2.3_Scientific_Revision.docx` (27 October 2026), Section 5 and 5.1, was compared with the unchanged source file `QRUM_OpticalClock_Synthetic_Benchmark_v2.2.py`. The script was executed locally with Python and NumPy and deterministic unit/regression tests were run.

| Manuscript claim | Confirmed by script/run? | Reference result |
| --- | --- | --- |
| Synthetic frequency f_b = 0.010 Hz | Yes | 0.010 Hz |
| Time grid Δt = 1 s; 10,000 samples | Yes | 1 s; N=10000 |
| Fictional sensitivity differences ΔK12=0.5, ΔK13=1.5 | Yes | [0.5, 1.5] |
| Injected g=2.000 × 10^-17 | Yes | 2.000e-17 |
| Ideal ratio amplitudes = 1.000e-17 and 3.000e-17 | Yes | [1.000e-17, 3.000e-17] |
| Per-clock noise σ=1.000 × 10^-16 per one-second sample | Yes | 1.000e-16 |
| Random seed 20261027 | Yes | 20261027 |
| Shared-clock correlation included | Yes | C_ratio = σ² [[2,1],[1,2]] |
| GLS recovered g≈2.060 × 10^-17 | Yes | 2.060e-17 |
| Nulls = 2000; empirical fixed-frequency 1% threshold≈3.869e-18 | Yes | 2000; 3.869e-18 |
| Injections=1000; detection fraction=1.000 | Yes | 1000; 1.000 |
| Instrument transfer H12=H13=1 | Assumed only, not instrument-calibrated | Simplifying simulation assumption |

## Numerical/statistical checks

- The projection weights obey `ratio_weights @ DK = 1`, preserving the injected signal amplitude.
- Ratio noise is correctly correlated because both ratios use clock 1; covariance is `σ² [[2,1],[1,2]]`.
- The analytic 1% fixed-frequency amplitude threshold for this idealized Gaussian model is approximately `3.974e-18`; the finite 2,000-null Monte Carlo estimate is `3.869e-18`, a plausible finite-sample fluctuation.
- The positive fitted amplitude is a noisy estimator and does not need to equal the injected value exactly.

## Limitations of the verification

- The test validates **internal numerical reproducibility**, not any real-world QRUM effect.
- No experimental clock measurement, calibrated atomic sensitivity coefficients, measured response `H(f)`, real noise covariance, or physical upper limit was available for this comparison.
- The null threshold is estimated at a single *prespecified* 0.010 Hz frequency. A scanned-frequency trial would require a global multiplicity correction.
- The finite Monte Carlo count limits threshold precision; the perfect 1000/1000 injected recovery is contingent on the chosen artificial noise and amplitude.
- The manuscript specifies a more general future procedure than this demonstration script implements; nuisance-regressor fitting, real H(f), full end-to-end calibrated injection recovery and a 95% physical limit remain future tasks.

**Status:** Consistent and suitable for a reproducibility-code upload **as a synthetic benchmark**. Not a validated physical prediction or experimental result.
