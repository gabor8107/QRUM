from pathlib import Path
import numpy as np
from scipy import signal

def main():
    out=Path('data'); out.mkdir(exist_ok=True); fs=4096.0; duration=32.0; n=int(fs*duration); rng=np.random.default_rng(20260727); t=np.arange(n)/fs
    white=rng.normal(0,1,n); colored=signal.lfilter([1.0],[1.0,-0.96],white); colored/=np.std(colored)
    tau=t-16.0; envelope=np.exp(-0.5*(tau/0.18)**2); phase=2*np.pi*(45*tau+110*tau**2); template=1.8*envelope*np.sin(phase)
    resonance=0.16*signal.windows.tukey(n,alpha=.1)*np.sin(2*np.pi*150*t); strain=colored+template+resonance
    np.save(out/'demo_strain.npy',strain); np.save(out/'demo_template.npy',template); print('Demo data created.')
if __name__=='__main__': main()
