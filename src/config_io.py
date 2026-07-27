from pathlib import Path
import yaml

def load_config(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Configuration file not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError("Configuration must be a mapping.")
    for key in ("project", "data", "preprocessing", "psd", "fit"):
        if key not in cfg:
            raise ValueError(f"Missing configuration section: {key}")
    return cfg
