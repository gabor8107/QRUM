import numpy as np
from .fitting import fit_residual_spectrum

def bootstrap_fit(frequencies,power,fitted_values,residuals,iterations,seed,f0_bounds,q_bounds,amplitude_bounds,baseline_kind,use_log_power):
    rng=np.random.default_rng(seed); samples={'amplitude':[],'f0_hz':[],'quality_factor':[]}
    for _ in range(iterations):
        synthetic=fitted_values+rng.choice(residuals,size=len(residuals),replace=True)
        if not use_log_power: synthetic=np.maximum(synthetic,np.finfo(float).tiny)
        try: fit=fit_residual_spectrum(frequencies,synthetic,f0_bounds,q_bounds,amplitude_bounds,baseline_kind,use_log_power)
        except Exception: continue
        for k in samples:
            if k in fit.parameters: samples[k].append(fit.parameters[k])
    out={}
    for k,v in samples.items():
        a=np.asarray(v,float)
        out[k]={'n':int(len(a)),'median':float(np.median(a)) if len(a) else None,'low_95':float(np.percentile(a,2.5)) if len(a) else None,'high_95':float(np.percentile(a,97.5)) if len(a) else None}
    return out
