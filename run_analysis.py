import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from src.bootstrap import bootstrap_fit
from src.config_io import load_config
from src.data_io import load_strain,load_template,save_json,select_segment
from src.fitting import fit_residual_spectrum
from src.line_exclusion import build_line_mask
from src.plotting import plot_spectrum_fit,plot_time_series
from src.preprocessing import preprocess_strain,subtract_template
from src.spectral import periodogram_power,welch_psd,whiten_frequency_domain

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',required=True); args=ap.parse_args(); c=load_config(args.config)
    pr,d,pc,ps,fc=c['project'],c['data'],c['preprocessing'],c['psd'],c['fit']; lc=c.get('line_exclusion',{}); bc=c.get('bootstrap',{}); plc=c.get('plots',{})
    stem=pr.get('output_stem','qrum_analysis'); Path('figures').mkdir(exist_ok=True); Path('results').mkdir(exist_ok=True)
    strain,fs=load_strain(d['strain_file'],d.get('dataset_path'),d.get('sample_rate')); strain=select_segment(strain,fs,float(d.get('start_time',0)),d.get('duration'))
    kwargs=dict(detrend_type=pc.get('detrend','linear'),highpass_hz=pc.get('highpass_hz'),lowpass_hz=pc.get('lowpass_hz'),filter_order=int(pc.get('filter_order',4)),taper_fraction=float(pc.get('taper_fraction',.02)))
    processed=preprocess_strain(strain,fs,**kwargs); template_scale=None
    if d.get('template_file'):
        template=preprocess_strain(load_template(d['template_file']),fs,**kwargs); residual,template_scale=subtract_template(processed,template); processed=processed[:len(residual)]; mode='template-subtracted residual'
    else: residual=processed.copy(); mode='detector-spectrum analysis without waveform subtraction'
    pf,pv=welch_psd(residual,fs,float(ps.get('nperseg_seconds',2)),float(ps.get('overlap_fraction',.5)),ps.get('window','hann')); white=whiten_frequency_domain(residual,fs,pf,pv); f,power=periodogram_power(white,fs)
    mask=(f>=float(fc['fmin_hz']))&(f<=float(fc['fmax_hz']))
    if lc.get('enabled',False): mask &= build_line_mask(f,[float(v) for v in lc.get('frequencies_hz',[])],float(lc.get('half_width_hz',1)))
    x,y=f[mask],power[mask]; use_log=bool(fc.get('use_log_power',False)); yfit=np.log(y) if use_log else y
    fit=fit_residual_spectrum(x,y,tuple(map(float,fc['f0_bounds_hz'])),tuple(map(float,fc['q_bounds'])),tuple(map(float,fc['amplitude_bounds'])),fc.get('baseline','linear'),use_log)
    boot=None
    if bc.get('enabled',False): boot=bootstrap_fit(x,y,fit.fitted_values,yfit-fit.fitted_values,int(bc.get('iterations',100)),int(bc.get('seed',20260727)),tuple(map(float,fc['f0_bounds_hz'])),tuple(map(float,fc['q_bounds'])),tuple(map(float,fc['amplitude_bounds'])),fc.get('baseline','linear'),use_log)
    payload={'project':pr.get('name'),'analysis_mode':mode,'sample_rate_hz':fs,'samples_analyzed':int(len(residual)),'duration_seconds':float(len(residual)/fs),'template_scale':template_scale,'fit':fit.as_dict(),'bootstrap':boot,'configuration_file':args.config}
    save_json(Path('results')/f'{stem}_summary.json',payload)
    pd.DataFrame({'frequency_hz':x,'power':y,'baseline_fit':fit.baseline_values,'resonance_fit':fit.resonance_values,'total_fit':fit.fitted_values}).to_csv(Path('results')/f'{stem}_spectrum.csv',index=False)
    plot_spectrum_fit(x,yfit if use_log else y,fit.fitted_values,fit.baseline_values,fit.parameters['f0_hz'],Path('figures')/f'{stem}_spectrum_fit.png',f"{pr.get('name')} — {mode}",int(plc.get('dpi',180)),bool(plc.get('log_x',False)),bool(plc.get('log_y',True)),use_log)
    t=np.arange(len(residual))/fs; plot_time_series(t,processed,residual,Path('figures')/f'{stem}_time_series.png',f"{pr.get('name')} — time domain",int(plc.get('dpi',180)))
    print(f"Analysis complete: {mode}"); print(f"Estimated f0: {fit.parameters['f0_hz']:.3f} Hz"); print(f"Estimated Q: {fit.parameters['quality_factor']:.3f}"); print(f"Delta AICc: {fit.as_dict()['delta_aicc_null_minus_resonance']:.3f}")
if __name__=='__main__': main()
