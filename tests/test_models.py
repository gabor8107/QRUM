import numpy as np
from src.model_comparison import information_criteria
from src.resonance_model import lorentzian_component,resonance_factor

def test_center(): assert np.isclose(resonance_factor(np.array([150.]),.2,150.,30.)[0],1.2)
def test_half_max():
    f0=150.;q=30.;w=f0/q;v=lorentzian_component(np.array([f0,f0+w]),2.,f0,q);assert np.isclose(v[0],2.) and np.isclose(v[1],1.)
def test_ic(): assert all(np.isfinite(v) for v in information_criteria(10.,100,4).values())
