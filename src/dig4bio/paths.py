import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"
FIGURES_FOLDER = PROJECT_ROOT / "results" / "figures"

RAW_DATA_FOLDER = DATA_FOLDER / "raw"
INTERIM_DATA_FOLDER = DATA_FOLDER / "interim"
PROCESSED_DATA_FOLDER = DATA_FOLDER / "processed"

FIGURES_EDA_FOLDER = FIGURES_FOLDER / "eda"