import numpy as np

def build_line_mask(frequencies,line_frequencies_hz,half_width_hz):
    mask=np.ones_like(frequencies,dtype=bool)
    for line in line_frequencies_hz: mask &= np.abs(frequencies-float(line))>half_width_hz
    return mask
