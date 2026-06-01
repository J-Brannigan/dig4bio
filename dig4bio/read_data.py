import pandas as pd
from pathlib import Path
from dig4bio.paths import RAW_DATA_FOLDER


def read_raman_file(file_name: str, level: str) -> pd.DataFrame:

    folder_map = {
        'raw': RAW_DATA_FOLDER
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