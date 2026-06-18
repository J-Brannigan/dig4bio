from pathlib import Path
import pandas as pd
from dig4bio.paths import RAW_DATA_FOLDER, INTERIM_DATA_FOLDER, PROCESSED_DATA_FOLDER


def get_level_path (level: str) -> Path:

    folder_map = {
        'raw': RAW_DATA_FOLDER,
        'interim': INTERIM_DATA_FOLDER,
        'processed': PROCESSED_DATA_FOLDER
    }

    return folder_map[level]

def get_interim_spectral_cols(device: str, df: pd.DataFrame) -> list[str]:
    """Return spectral column names for an interim dataset.

    Interim source-device, transfer plate, and test datasets have different
    metadata/label columns, so the spectral columns occupy different slices.
    """
    if device == 'transfer_plate':
        spectral_cols = df.columns[1:-4]
    elif device == '96_samples':
        spectral_cols = df.columns[1:]
    else:
        spectral_cols = df.columns[:-5]

    return spectral_cols.tolist()