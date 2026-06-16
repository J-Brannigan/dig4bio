import pandas as pd
from dig4bio.utils import get_level_path
from pathlib import Path
from dig4bio.constants import DATASET_NAME_ALIASES

def read_raman_file(name: str, level: str, header: int | None = 0) -> pd.DataFrame:

    DATASET_NAME_ALIASES

    folder = get_level_path(level)

    candidates = [
        folder / name,
        folder / f"{name}.csv",
    ]

    if name in DATASET_NAME_ALIASES:
        candidates.append(folder / f"{DATASET_NAME_ALIASES[name]}.csv")

    for file_path in candidates:
        if file_path.exists():
            return pd.read_csv(file_path,index_col=False, header=header)
    
    raise FileNotFoundError(name)

def write_raman_file(df: pd.DataFrame, level: Path, output_filename: str) -> None:

    folder = get_level_path(level)

    if output_filename.lower().strip().endswith('.csv'):
        df.to_csv(folder / output_filename, index=False)
    elif output_filename.lower().strip().endswith('.parquet'):
        df.to_parquet(folder / output_filename, index=False)
    else:
        raise ValueError(f'Unsupported or missing filetype: {output_filename}')

    return