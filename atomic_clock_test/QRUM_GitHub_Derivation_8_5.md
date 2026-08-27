# QRUM Atomic Clock Prospective Test Region

## Phenomenological Derivation and Open-Science Rationale

### Purpose

This document provides a conservative phenomenological justification for the prospective QRUM atomic-clock test region discussed in Section 8.5. It is not presented as a derivation from a fundamental theory and does not claim detection of new physics.

### Starting Point

QRUM Phase-1 uses a localized spectral response function as a phenomenological analysis template:

\[
f_\phi(f)=1+\frac{\alpha}{1+\left(\frac{f-f_r}{\Gamma}\right)^2}
\]

where:

- α = dimensionless amplitude parameter
- f_r = central test frequency
- Γ = characteristic width

The Lorentzian form is used because it provides a simple, localized narrow-band model that can be tested against data.

### Why a Predefined Test Region?

A major risk in exploratory data analysis is the look-elsewhere effect.
To reduce post-hoc interpretation, a restricted frequency interval may be defined before performing a decisive test.

For QRUM-related exploratory studies, the following interval has been selected:

\[
145\;Hz \le f \le 155\;Hz
\]

This interval should be interpreted only as a preregistered test region.
It is not evidence for a physical resonance and is not claimed to be a fundamental constant.

### Connection to Optical Atomic Clocks

Optical atomic clocks measure fractional-frequency variations:

\[
y(t)=\Delta f/f
\]

Current state-of-the-art systems can probe sensitivities approaching:

\[
10^{-18}\;to\;10^{-19}
\]

Therefore, if a future QRUM formulation predicts a measurable clock signature within this sensitivity range, differential clock comparisons provide a direct experimental test.

### Testable Expectation

The framework makes only the following limited expectation:

1. Any genuine narrow-band residual effect should appear more consistently within a predefined search window than in broadband random noise.
2. Independent experiments should recover statistically compatible results.
3. Improved sensitivity should either strengthen evidence or progressively constrain the parameter space.
4. Repeated null results reduce the viability of the tested phenomenological realization.

### Falsifiability

If a future QRUM-derived prediction specifies:

- observable,
- frequency range,
- amplitude model,
- detection criterion,

and sufficiently sensitive measurements fail to observe the predicted signature, then that specific implementation is constrained or falsified within the tested domain.

### Open Science Statement

All hypotheses, analysis choices, and software implementations should be made openly available whenever possible. Independent reproduction is encouraged. Reproducibility is considered more important than positive outcomes.

---

Author: P. Gabor

Suggested use: GitHub README, supplementary note, or methodological appendix.
