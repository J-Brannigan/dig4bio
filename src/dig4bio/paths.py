import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_DATA_FOLDER = DATA_FOLDER / "raw"
INTERIM_DATA_FOLDER = DATA_FOLDER / "interim"
PROCESSED_DATA_FOLDER = DATA_FOLDER / "processed"