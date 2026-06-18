import pandas as pd

from dig4bio.utils import get_level_path
from dig4bio.constants import DATASET_NAME_ALIASES


def read_raman_file(name: str, level: str, header: int | None = 0) -> pd.DataFrame:
    """
    Read a Raman spectrum dataset from a raw, interim, or processed data folder.

    The name is attempted literally first, then with extension added, then using
    the alias mapping (e.g. mettler -> mettler_toledo.csv).
    
    Parameters
    ----------
    name: str
        The filename or alias of the file to read from
    level: str
        The data maturity level (raw/interim/processed)
    header: int | None
        Row number corresponding to the header row, or None if no header row
    Returns
    -------
    pd.DataFrame
        The Raman spectrum dataset as a dataframe
    """

    folder = get_level_path(level)

    # Try exact names first, then known project aliases such as mettler -> mettler_toledo.csv.
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

def write_raman_file(df: pd.DataFrame, level: str, output_filename: str) -> None:
    """
    Write a Raman spectrum dataset to a file
    
    Parameters
    ----------
    df: pd.DataFrame
        The Raman dataset dataframe to write to a file
    level: str
        The data maturity level (raw/interim/processed)
    output_filename: str
        The filename of the file to write the Raman dataset to
    """
    folder = get_level_path(level)

    if output_filename.lower().strip().endswith('.csv'):
        df.to_csv(folder / output_filename, index=False)
    elif output_filename.lower().strip().endswith('.parquet'):
        df.to_parquet(folder / output_filename, index=False)
    else:
        raise ValueError(f'Unsupported or missing filetype: {output_filename}')
