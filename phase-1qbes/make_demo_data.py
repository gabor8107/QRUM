"""Generate a synthetic residual spectrum for pipeline testing (no Lorentzian)."""
from pathlib import Path
import numpy as np
import pandas as pd


def main():
    out = Path("data")
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(20260803)

    f = np.linspace(40, 400, 1800)

    # Smooth baseline (1/f-like + constant)
    baseline = 1e-23 * (1 + 30 / (f / 100))

    # Noise only – no injected peak profile
    noise = rng.normal(0, 0.4e-24, size=f.shape)
    power = baseline + np.abs(noise)

    df = pd.DataFrame({
        "frequency_Hz": f,
        "power": power,
        "baseline_true": baseline,
    })
    df.to_csv(out / "demo_residual_spectrum.csv", index=False)
    print("Demo residual spectrum written: data/demo_residual_spectrum.csv")


if __name__ == "__main__":
    main()
