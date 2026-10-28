"""QRUM-motivated optical-clock conditional benchmark, v2.2.

This is a synthetic varying-alpha clock-ratio injection test, NOT a QRUM
physical prediction and NOT an analysis of real atomic-clock measurements.
No nonstandard model is validated by successful recovery of injected data.

Requires: numpy. Reproducible with seed 20261027.
"""
import numpy as np

SEED = 20261027
FREQUENCY_HZ = 0.01
DT_S = 1.0
N = 10000
G_INJECTED = 2e-17
PHASE_RAD = 0.6
SIGMA_INDIVIDUAL_CLOCK = 1e-16  # fictional white per-sample fractional noise
K = np.array([1.5, 1.0, 0.0])  # synthetic—not coefficients of real species
DK = np.array([K[0] - K[1], K[0] - K[2]])
NSIM_NULL = 2000
NSIM_INJECTED = 1000
FALSE_POSITIVE_ALPHA = 0.01

rng = np.random.default_rng(SEED)
t = np.arange(N) * DT_S
w = 2 * np.pi * FREQUENCY_HZ
basis = np.column_stack((np.cos(w * t), np.sin(w * t)))
# A single clock is shared by both ratios. Do not treat ratio noises as independent.
C_ratio = SIGMA_INDIVIDUAL_CLOCK**2 * np.array([[2., 1.], [1., 2.]])
# GLS scalar combination preserves signal and the shared-reference covariance.
C0 = np.array([[2., 1.], [1., 2.]])
invC0 = np.linalg.inv(C0)
ratio_weights = (DK @ invC0) / (DK @ invC0 @ DK)
noise_std_of_projection = SIGMA_INDIVIDUAL_CLOCK / np.sqrt(DK @ invC0 @ DK)

# The full two-ratio procedure is algebraically equivalent to the GLS projection
# to a one-channel white process, followed by two-quadrature linear regression.
def estimate_g(y12, y13):
    projected = ratio_weights[0] * y12 + ratio_weights[1] * y13
    c, s = np.linalg.lstsq(basis, projected, rcond=None)[0]
    return float(np.hypot(c, s)), float(np.arctan2(-s, c))

def simulation(g):
    # Independent mock clock noise; pair ratios share clock 1.
    eps = rng.normal(0., SIGMA_INDIVIDUAL_CLOCK, (3, N))
    signal = g * np.cos(w * t + PHASE_RAD)
    y1, y2, y3 = (K[:, None] * signal[None, :] + eps)
    return estimate_g(y1 - y2, y1 - y3)

fitted_g, fitted_phase = simulation(G_INJECTED)
null_g = np.array([simulation(0.)[0] for _ in range(NSIM_NULL)])
threshold = float(np.quantile(null_g, 1.0 - FALSE_POSITIVE_ALPHA))
injected_g = np.array([simulation(G_INJECTED)[0] for _ in range(NSIM_INJECTED)])
recovery_power = float(np.mean(injected_g > threshold))

print('This example uses invented clocks and invented data, NOT measured results.')
print(f'Input frequency = {FREQUENCY_HZ:.3f} Hz, N = {N}, dt = {DT_S:.1f} s')
print(f'Synthetic response differences = {DK[0]:.1f}, {DK[1]:.1f}')
print(f'Predicted ideal output amplitudes = {abs(DK[0])*G_INJECTED:.3e}, {abs(DK[1])*G_INJECTED:.3e}')
print(f'Injected g = {G_INJECTED:.3e}, fitted g = {fitted_g:.3e}, fitted phase = {fitted_phase:.4f} rad')
print(f'Simulated 1% false-positive threshold (single fixed frequency) = {threshold:.3e}')
print(f'Simulated detection probability at injected g = {recovery_power:.3f}')
print('No experimental upper limit or QRUM constraint is inferred.')
