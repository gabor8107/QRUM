import numpy as np
from scipy import signal

def welch_psd(x,fs,nperseg_seconds=2.0,overlap_fraction=0.5,window='hann'):
    nper=min(max(32,int(round(nperseg_seconds*fs))),len(x)); nover=int(round(overlap_fraction*nper))
    f,p=signal.welch(x,fs=fs,window=window,nperseg=nper,noverlap=nover,detrend='constant',scaling='density',average='median')
    return f,np.maximum(p,np.finfo(float).tiny)

def whiten_frequency_domain(x,fs,pf,psd):
    n=len(x); spec=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/fs)
    ip=np.interp(f,pf,psd,left=psd[0],right=psd[-1]); y=np.fft.irfft(spec/np.sqrt(np.maximum(ip,np.finfo(float).tiny)),n=n)
    s=np.std(y)
    return y/s if s>0 else y

def periodogram_power(x,fs):
    f,p=signal.periodogram(x,fs=fs,window='hann',detrend='constant',scaling='density')
    return f,np.maximum(p,np.finfo(float).tiny)
