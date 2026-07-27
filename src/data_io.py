from pathlib import Path
import json
import h5py
import numpy as np
import pandas as pd

COMMON = ("strain/Strain", "/strain/Strain", "strain", "/strain", "data/strain", "/data/strain")

def _validate(x):
    x = np.asarray(x, dtype=float).squeeze()
    if x.ndim != 1: raise ValueError("Input must be one-dimensional.")
    if not np.all(np.isfinite(x)): raise ValueError("Input contains NaN or infinity.")
    return x

def _find_dataset(h):
    found=[]
    def visit(name,obj):
        if isinstance(obj,h5py.Dataset) and obj.ndim==1 and np.issubdtype(obj.dtype,np.number): found.append(name)
    h.visititems(visit)
    if not found: raise ValueError("No 1D numeric HDF5 dataset found.")
    return max(found,key=lambda n:h[n].shape[0])

def _sample_rate(h,ds):
    for container in (ds.attrs,h.attrs):
        for name in ("sample_rate","sampling_rate","SampleRate","fs"):
            if name in container:
                v=float(np.asarray(container[name]).squeeze())
                if v>0:return v
        for name in ("Xspacing","delta_t","dt"):
            if name in container:
                v=float(np.asarray(container[name]).squeeze())
                if v>0:return 1.0/v
    return None

def load_strain(file_path,dataset_path=None,sample_rate=None):
    p=Path(file_path)
    if not p.exists(): raise FileNotFoundError(f"Strain file not found: {p}")
    s=p.suffix.lower()
    if s=='.npy':
        if sample_rate is None: raise ValueError("Set data.sample_rate for .npy files.")
        return _validate(np.load(p)),float(sample_rate)
    if s in ('.csv','.txt'):
        x=pd.read_csv(p).select_dtypes(include=[np.number]).iloc[:,-1].to_numpy() if s=='.csv' else np.loadtxt(p)
        if sample_rate is None: raise ValueError("Set data.sample_rate for text files.")
        return _validate(x),float(sample_rate)
    if s not in ('.hdf5','.h5'): raise ValueError(f"Unsupported extension: {s}")
    with h5py.File(p,'r') as h:
        chosen=dataset_path or next((c for c in COMMON if c in h),None) or _find_dataset(h)
        ds=h[chosen]; x=np.asarray(ds[()]); detected=_sample_rate(h,ds)
    rate=float(sample_rate) if sample_rate is not None else detected
    if rate is None: raise ValueError("Sample rate not found; set data.sample_rate in YAML.")
    return _validate(x),rate

def load_template(file_path):
    p=Path(file_path); s=p.suffix.lower()
    if s=='.npy': x=np.load(p)
    elif s=='.txt': x=np.loadtxt(p)
    elif s=='.csv': x=pd.read_csv(p).select_dtypes(include=[np.number]).iloc[:,-1].to_numpy()
    else: raise ValueError("Template must be .npy, .csv or .txt")
    return _validate(x)

def select_segment(x,fs,start_time,duration):
    a=max(0,int(round(start_time*fs))); b=len(x) if duration is None else a+int(round(duration*fs))
    y=x[a:min(b,len(x))]
    if len(y)<max(32,int(fs)): raise ValueError("Selected segment is too short.")
    return y

def save_json(path,payload):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8') as f: json.dump(payload,f,indent=2,ensure_ascii=False)
