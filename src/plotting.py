from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def plot_spectrum_fit(f,power,fitted,baseline,f0_hz,output_path,title,dpi=180,log_x=False,log_y=True,use_log_power=False):
    p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True)
    observed=np.exp(power) if use_log_power else power; fitv=np.exp(fitted) if use_log_power else fitted; basev=np.exp(baseline) if use_log_power else baseline
    plt.figure(figsize=(8,5)); plt.plot(f,observed,lw=.9,label='Observed spectrum'); plt.plot(f,basev,lw=1.4,label='Null baseline'); plt.plot(f,fitv,lw=1.4,label='Baseline + Lorentzian'); plt.axvline(f0_hz,ls='--',lw=1,label=f'f0 = {f0_hz:.2f} Hz'); plt.xlabel('Frequency [Hz]'); plt.ylabel('Power spectral density'); plt.title(title)
    if log_x: plt.xscale('log')
    if log_y: plt.yscale('log')
    plt.legend(); plt.tight_layout(); plt.savefig(p,dpi=dpi); plt.close()

def plot_time_series(time,strain,residual,output_path,title,dpi=180):
    p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True); n=min(len(time),len(strain),len(residual))
    plt.figure(figsize=(8,5)); plt.plot(time[:n],strain[:n],lw=.7,label='Processed strain'); plt.plot(time[:n],residual[:n],lw=.7,label='Residual'); plt.xlabel('Time [s]'); plt.ylabel('Normalized amplitude'); plt.title(title); plt.legend(); plt.tight_layout(); plt.savefig(p,dpi=dpi); plt.close()
