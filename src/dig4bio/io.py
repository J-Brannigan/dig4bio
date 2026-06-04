import pandas as pd
from dig4bio.utils import get_level_path
from pathlib import Path

def read_raman_file(name: str, level: str) -> pd.DataFrame:

    abbr_map = {
        'anton532': 'anton_532',
        'anton785': 'anton_785',
        'mettler':  'mettler_toledo',
        'tec' :     'tec5',
        'transfer': 'transfer_plate',
        '96':       '96_samples'
    }

    folder = get_level_path(level)

    candidates = [
        folder / name,
        folder / f"{name}.csv",
    ]

    if name in abbr_map:
        candidates.append(folder / f"{abbr_map[name]}.csv")

    for file_path in candidates:
        if file_path.exists():
            return pd.read_csv(file_path)
    
    raise FileNotFoundError(name)

def write_raman_file(df: pd.DataFrame, level: Path, output_filename: str) -> None:

    folder = get_level_path(level)

    if output_filename.lower().strip().endswith('.csv'):
        df.to_csv(folder / output_filename)
    elif output_filename.lower().strip().endswith('.parquet'):
        df.to_parquet(folder / output_filename)
    else:
        raise ValueError(f'Unsupported or missing filetype: {output_filename}')

    return