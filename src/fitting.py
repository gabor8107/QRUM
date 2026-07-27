from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit
from .model_comparison import information_criteria
from .resonance_model import linear_baseline,lorentzian_component

@dataclass
class FitResult:
    baseline_kind:str; parameters:dict; covariance:np.ndarray; fitted_values:np.ndarray; baseline_values:np.ndarray; resonance_values:np.ndarray; metrics_null:dict; metrics_resonance:dict
    def as_dict(self):
        return {'baseline_kind':self.baseline_kind,'parameters':self.parameters,'metrics_null':self.metrics_null,'metrics_resonance':self.metrics_resonance,'delta_aicc_null_minus_resonance':self.metrics_null['aicc']-self.metrics_resonance['aicc'],'delta_bic_null_minus_resonance':self.metrics_null['bic']-self.metrics_resonance['bic']}

def fit_residual_spectrum(frequencies,power,f0_bounds,q_bounds,amplitude_bounds,baseline_kind='linear',use_log_power=False):
    x=np.asarray(frequencies,float); yraw=np.asarray(power,float); y=np.log(yraw) if use_log_power else yraw
    if len(x)<20: raise ValueError("Too few spectral bins")
    pivot=float(np.median(x)); f0g=float(np.clip(x[np.argmax(y)],*f0_bounds)); ag=float(max(np.percentile(y,99)-np.median(y),np.std(y))); ag=float(np.clip(ag,amplitude_bounds[0]+1e-15,amplitude_bounds[1])); qg=float(np.sqrt(q_bounds[0]*q_bounds[1])); og=float(np.median(y))
    if baseline_kind=='constant':
        def null(f,o): return np.full_like(f,o)
        def model(f,o,a,f0,q): return o+lorentzian_component(f,a,f0,q)
        np0,_=curve_fit(null,x,y,p0=[og],maxfev=20000)
        popt,pcov=curve_fit(model,x,y,p0=[og,ag,f0g,qg],bounds=([-np.inf,amplitude_bounds[0],f0_bounds[0],q_bounds[0]],[np.inf,amplitude_bounds[1],f0_bounds[1],q_bounds[1]]),maxfev=50000)
        base=null(x,popt[0]); res=lorentzian_component(x,popt[1],popt[2],popt[3]); fit=base+res; nullfit=null(x,*np0); names=('offset','amplitude','f0_hz','quality_factor'); kn,kr=1,4
    else:
        def null(f,o,s): return linear_baseline(f,o,s,pivot)
        def model(f,o,s,a,f0,q): return linear_baseline(f,o,s,pivot)+lorentzian_component(f,a,f0,q)
        np0,_=curve_fit(null,x,y,p0=[og,0.0],maxfev=20000)
        popt,pcov=curve_fit(model,x,y,p0=[og,0.0,ag,f0g,qg],bounds=([-np.inf,-np.inf,amplitude_bounds[0],f0_bounds[0],q_bounds[0]],[np.inf,np.inf,amplitude_bounds[1],f0_bounds[1],q_bounds[1]]),maxfev=50000)
        base=linear_baseline(x,popt[0],popt[1],pivot); res=lorentzian_component(x,popt[2],popt[3],popt[4]); fit=base+res; nullfit=null(x,*np0); names=('offset','slope','amplitude','f0_hz','quality_factor'); kn,kr=2,5
    params={n:float(v) for n,v in zip(names,popt)}; params['pivot_hz']=pivot; params['use_log_power']=bool(use_log_power)
    return FitResult(baseline_kind,params,pcov,fit,base,res,information_criteria(np.sum((y-nullfit)**2),len(x),kn),information_criteria(np.sum((y-fit)**2),len(x),kr))
