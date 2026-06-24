import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"
FIGURES_FOLDER = PROJECT_ROOT / "results" / "figures"
CONFIGS_FOLDER = PROJECT_ROOT / "configs"

# DATA
RAW_DATA_FOLDER = DATA_FOLDER / "raw"
INTERIM_DATA_FOLDER = DATA_FOLDER / "interim"
PROCESSED_DATA_FOLDER = DATA_FOLDER / "processed"

# FIGURES
FIGURES_EDA_FOLDER = FIGURES_FOLDER / "eda"

# CONFIG
EXPERIMENTS_CONFIG_FOLDER = CONFIGS_FOLDER / "experiments"
PREPROCESSING_CONFIG_FOLDER = CONFIGS_FOLDER / "preprocessing"

def get_level_path(level: str) -> Path:

    folder_map = {
        'raw': RAW_DATA_FOLDER,
        'interim': INTERIM_DATA_FOLDER,
        'processed': PROCESSED_DATA_FOLDER
    }

    return folder_map[level]

def get_configs_path(config_type: str) -> Path:

    folder_map = {
        "experiments": EXPERIMENTS_CONFIG_FOLDER,
        "preprocessing": PREPROCESSING_CONFIG_FOLDER
    }

    return folder_map[config_type]