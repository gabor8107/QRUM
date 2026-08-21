# Statistical Survey of Compact Object Frequency Distributions

**Author:** P. Gabor (Independent Researcher)  
**Version:** 2.1  
**License:** CC BY 4.0  

Reproducible statistical pipeline for comparing frequency distributions of compact-object classes (pulsating white dwarfs, pulsars, magnetars, black-hole HFQPOs) using identical non-parametric and mixture-modelling methods.

## Contents

```
data/           curated frequency tables and object lists
src/            Python analysis scripts (KDE, GMM, BIC, bootstrap)
notebooks/      example Jupyter notebooks
figures/        output plots
docs/           supplementary notes
```

## Scientific scope

This repository implements a uniform statistical workflow:

1. Kernel Density Estimation (KDE)
2. Gaussian Mixture Modelling (GMM) with BIC model selection
3. Object-level bootstrap and sensitivity tests
4. Cross-class comparison of frequency organisation

The analysis is exploratory and methodological. It quantifies structure in publicly available catalogues and documents selection effects and sample limitations. No claim is made that observed statistical features require a common physical mechanism.

## Research context

This work was originally developed within the broader Quantum Resonance Unified Model (QRUM) research programme. The statistical analysis and results presented here are formulated independently of that theoretical framework and are not interpreted as evidence for or validation of QRUM.

## Data sources (public)

- Montreal White Dwarf Database (MWDD) + literature (pulsating WDs)
- ATNF Pulsar Catalogue
- Published magnetar timing / oscillation data
- Literature HFQPO measurements for stellar-mass black holes

Curated tables used in the analysis are placed in `data/`.

## Quick start

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

python src/run_pipeline.py
```

## Citation

If you use this code or the curated tables, please cite the corresponding Zenodo / OSF preprint and this repository.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0)
