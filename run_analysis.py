#!/usr/bin/env python3
"""QRUM Correlation Framework — main entry point."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

from src.config_io import load_config
from src.data_io import load_strain, select_segment
from src.preprocessing import preprocess_strain
from src.spectral import welch_psd, periodogram_power, whiten_frequency_domain
from src.fitting import fit_residual_spectrum
from src.bootstrap import bootstrap_fit
from src.line_exclusion import build_line_mask
from src.plotting import plot_spectrum_fit, plot_time_series

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    c = load_config(args.config)

    pr = c["project"]
    d = c["data"]
    pc = c["preprocessing"]
    ps = c["psd"]
    fc = c["fit"]
    lc = c.get("line_exclusion", {})
    bc = c.get("bootstrap", {})
    plc = c.get("plots", {})

    stem = pr.get("output_stem", "qrum_corr")
    Path("figures").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)

    # Load H1 (or single) strain
    strain_h, fs = load_strain(d["strain_h1"], d.get("sample_rate"))
    strain_h = select_segment(strain_h, fs, float(d.get("start_time", 0)), d.get("duration"))

    kwargs = dict(
        detrend_type=pc.get("detrend", "linear"),
        highpass_hz=pc.get("highpass_hz"),
        lowpass_hz=pc.get("lowpass_hz"),
        filter_order=int(pc.get("filter_order", 4)),
        taper_fraction=float(pc.get("taper_fraction", 0.02)),
    )
    processed = preprocess_strain(strain_h, fs, **kwargs)

    # Optional template
    residual = processed.copy()
    mode = "detector-spectrum analysis"
    if d.get("template_file"):
        template = preprocess_strain(np.load(d["template_file"]), fs, **kwargs)
        # Simple scale match
        scale = np.dot(processed, template) / (np.dot(template, template) + 1e-30)
        residual = processed - scale * template
        mode = "template-subtracted residual"

    # PSD and whitening
    pf, pv = welch_psd(residual, fs, float(ps.get("nperseg_seconds", 2)), float(ps.get("overlap_fraction", 0.5)), ps.get("window", "hann"))
    white = whiten_frequency_domain(residual, fs, pf, pv)
    f, power = periodogram_power(white, fs)

    mask = (f >= float(fc["fmin_hz"])) & (f <= float(fc["fmax_hz"]))
    if lc.get("enabled", False):
        mask &= build_line_mask(f, [float(v) for v in lc.get("frequencies_hz", [])], float(lc.get("half_width_hz", 1)))

    x, y = f[mask], power[mask]
    fit = fit_residual_spectrum(x, y, tuple(map(float, fc["f0_bounds_hz"])), tuple(map(float, fc["q_bounds"])), tuple(map(float, fc["amplitude_bounds"])), fc.get("baseline", "linear"), False)

    boot = None
    if bc.get("enabled", False):
        boot = bootstrap_fit(x, y, fit.fitted_values, y - fit.fitted_values, int(bc.get("iterations", 100)), int(bc.get("seed", 20260728)), tuple(map(float, fc["f0_bounds_hz"])), tuple(map(float, fc["q_bounds"])), tuple(map(float, fc["amplitude_bounds"])), fc.get("baseline", "linear"), False)

    # Save
    import json
    payload = {
        "project": pr.get("name"),
        "analysis_mode": mode,
        "sample_rate_hz": fs,
        "samples_analyzed": int(len(residual)),
        "fit": fit.as_dict(),
        "bootstrap": boot,
    }
    with open(Path("results") / f"{stem}_summary.json", "w") as fp:
        json.dump(payload, fp, indent=2)

    pd.DataFrame({
        "frequency_hz": x,
        "power": y,
        "baseline_fit": fit.baseline_values,
        "resonance_fit": fit.resonance_values,
        "total_fit": fit.fitted_values,
    }).to_csv(Path("results") / f"{stem}_spectrum.csv", index=False)

    plot_spectrum_fit(x, y, fit.fitted_values, fit.baseline_values, fit.parameters["f0_hz"], Path("figures") / f"{stem}_spectrum_fit.png", f"{pr.get('name')} — {mode}", int(plc.get("dpi", 160)), False, bool(plc.get("log_y", True)), False)
    t = np.arange(len(residual)) / fs
    plot_time_series(t, processed, residual, Path("figures") / f"{stem}_time_series.png", f"{pr.get('name')} — time domain", int(plc.get("dpi", 160)))

    print(f"Analysis complete: {mode}")
    print(f"Estimated f0: {fit.parameters['f0_hz']:.3f} Hz")
    print(f"Estimated Q: {fit.parameters['quality_factor']:.3f}")
    print(f"Delta AICc: {fit.as_dict()['delta_aicc_null_minus_resonance']:.3f}")

if __name__ == "__main__":
    main()
