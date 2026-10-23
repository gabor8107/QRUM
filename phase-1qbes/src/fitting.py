"""
Baseline fitting utilities only (diagnostic).

The linear baseline is NOT subtracted before the fixed-band excess
calculation. It is reported only for diagnostic / quality-check purposes.

No peak fitting.
No Lorentzian.
No free frequency parameter.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

from src.model import baseline_linear


def fit_linear_baseline(f: np.ndarray, p: np.ndarray) -> dict:
    """Fit a linear baseline P(f) = a + b*f (diagnostic only)."""
    f = np.asarray(f, dtype=float)
    p = np.asarray(p, dtype=float)
    mask = np.isfinite(f) & np.isfinite(p)
    f, p = f[mask], p[mask]

    if len(f) < 5:
        return {"success": False, "reason": "too few points"}

    def lin(ff, a, b):
        return baseline_linear(ff, a, b)

    try:
        popt, pcov = curve_fit(lin, f, p, p0=[np.median(p), 0.0])
        perr = np.sqrt(np.diag(pcov))
        return {
            "success": True,
            "a": float(popt[0]),
            "b": float(popt[1]),
            "a_err": float(perr[0]),
            "b_err": float(perr[1]),
            "popt": popt,
        }
    except Exception as e:
        return {"success": False, "reason": str(e)}


def aic_bic(y: np.ndarray, yhat: np.ndarray, k: int):
    """Gaussian AIC / BIC from residual sum of squares."""
    y = np.asarray(y)
    yhat = np.asarray(yhat)
    n = len(y)
    rss = np.sum((y - yhat) ** 2)
    if rss <= 0 or n <= k + 1:
        return np.nan, np.nan
    s2 = rss / n
    logL = -0.5 * n * (np.log(2 * np.pi) + np.log(s2) + 1)
    aic = 2 * k - 2 * logL
    bic = k * np.log(n) - 2 * logL
    return float(aic), float(bic)
