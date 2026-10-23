import numpy as np

def apply_line_mask(f, p, lines_Hz, half_width=1.0):
    """Set power to NaN around known instrumental lines."""
    f = np.asarray(f)
    p = np.asarray(p, dtype=float).copy()
    for line in lines_Hz:
        m = (f >= line - half_width) & (f <= line + half_width)
        p[m] = np.nan
    return p
