import numpy as np

def resonance_factor(frequency,alpha,f0,quality_factor):
    if f0<=0 or quality_factor<=0: raise ValueError("f0 and Q must be positive")
    f=np.asarray(frequency,dtype=float); width=f0/quality_factor
    return 1.0+alpha/(1.0+((f-f0)/width)**2)

def lorentzian_component(frequency,amplitude,f0,quality_factor):
    if f0<=0 or quality_factor<=0: raise ValueError("f0 and Q must be positive")
    f=np.asarray(frequency,dtype=float); width=f0/quality_factor
    return amplitude/(1.0+((f-f0)/width)**2)

def linear_baseline(frequency,offset,slope,pivot):
    f=np.asarray(frequency,dtype=float); return offset+slope*(f-pivot)
