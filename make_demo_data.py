"""Generate synthetic two-detector data with optional injected residual feature."""
from pathlib import Path
import numpy as np
from scipy import signal

def main():
    out = Path("data")
    out.mkdir(exist_ok=True)
    fs = 4096.0
    duration = 32.0
    n = int(fs * duration)
    rng = np.random.default_rng(20260728)
    t = np.arange(n) / fs

    # Coloured noise for two detectors
    def coloured_noise():
        white = rng.normal(0, 1, n)
        colored = signal.lfilter([1.0], [1.0, -0.96], white)
        return colored / np.std(colored)

    h = coloured_noise()
    l = coloured_noise()

    # Simple chirp-like template
    tau = t - 16.0
    envelope = np.exp(-0.5 * (tau / 0.18)**2)
    phase = 2 * np.pi * (45 * tau + 110 * tau**2)
    template = 1.6 * envelope * np.sin(phase)

    # Optional weak residual feature near 150 Hz (for pipeline test only)
    resonance = 0.12 * signal.windows.tukey(n, alpha=0.1) * np.sin(2 * np.pi * 150 * t)

    strain_h = h + template + 0.7 * resonance
    strain_l = l + template + 0.7 * resonance

    np.save(out / "demo_h1.npy", strain_h)
    np.save(out / "demo_l1.npy", strain_l)
    np.save(out / "demo_template.npy", template)
    print("Demo two-detector data created.")

if __name__ == "__main__":
    main()
