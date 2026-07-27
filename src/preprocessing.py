import numpy as np
from scipy import signal

def preprocess_strain(x,fs,detrend_type='linear',highpass_hz=20.0,lowpass_hz=500.0,filter_order=4,taper_fraction=0.02):
    x=signal.detrend(np.asarray(x,dtype=float),type=detrend_type)
    ny=fs/2
    if highpass_hz is not None and lowpass_hz is not None:
        if not (0<highpass_hz<lowpass_hz<ny): raise ValueError("Require 0 < highpass < lowpass < Nyquist")
        sos=signal.butter(filter_order,[highpass_hz,lowpass_hz],btype='bandpass',fs=fs,output='sos')
        x=signal.sosfiltfilt(sos,x)
    elif highpass_hz is not None:
        x=signal.sosfiltfilt(signal.butter(filter_order,highpass_hz,btype='highpass',fs=fs,output='sos'),x)
    elif lowpass_hz is not None:
        x=signal.sosfiltfilt(signal.butter(filter_order,lowpass_hz,btype='lowpass',fs=fs,output='sos'),x)
    if taper_fraction>0: x=x*signal.windows.tukey(len(x),alpha=2*taper_fraction)
    return x

def subtract_template(strain,template):
    n=min(len(strain),len(template)); x=np.asarray(strain[:n]); h=np.asarray(template[:n])
    den=float(np.dot(h,h))
    if den<=0: raise ValueError("Template has zero norm")
    scale=float(np.dot(x,h)/den)
    return x-scale*h,scale
