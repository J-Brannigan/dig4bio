import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_DATA_FOLDER = DATA_FOLDER / "raw"
INTERIM_DATA_FOLDER = DATA_FOLDER / "INTERIM"

TRANSFER_PLATE_PATH_INTERIM = INTERIM_DATA_FOLDER / "transfer_plate.csv"
TEST_SAMPLES_PATH_INTERIM = INTERIM_DATA_FOLDER / "96_samples.csv"
SAMPLE_SUBMISSION_PATH_INTERIM = INTERIM_DATA_FOLDER / "sample_submission.csv"

def read_raman_file(file_name: str, level: str) -> pd.DataFrame:

    folder_map = {
        'raw': RAW_DATA_FOLDER,
        'interim': INTERIM_DATA_FOLDER
    }

    abbr_map = {
        'anton532': 'anton_532',
        'anton785': 'anton_785',
        'mettler': 'mettler_toledo',
        'tec' : 'tec5'
    }

    folder = folder_map[level]

    candidates = [
        folder / file_name,
        folder / f"{file_name}.csv",
    ]

    if file_name in abbr_map:
        candidates.append(folder / f"{abbr_map[file_name]}.csv")

    for file_path in candidates:
        if file_path.exists():
            return pd.read_csv(file_path)
    
    raise FileNotFoundError(file_name)

def get_transfer_plate_df() -> pd.DataFrame:
    if TRANSFER_PLATE_PATH.exists():
            return pd.read_csv(TRANSFER_PLATE_PATH)
    
    raise FileNotFoundError(TRANSFER_PLATE_PATH)

def get_test_samples_df() -> pd.DataFrame:
    if TEST_SAMPLES_PATH.exists():
            return pd.read_csv(TEST_SAMPLES_PATH)
    
    raise FileNotFoundError(TEST_SAMPLES_PATH)