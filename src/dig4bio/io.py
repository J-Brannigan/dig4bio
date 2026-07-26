import pandas as pd
import yaml
from collections.abc import Iterable
import os
from pathlib import Path

from dig4bio.paths import get_level_path, get_configs_path
from dig4bio.constants import DATASET_NAME_ALIASES
from dig4bio.paths import PREPROCESSING_CONFIG_FOLDER

def read_raman_file(name: str, level: str, header: int | None = 0, subfolder: str | None = None) -> pd.DataFrame:
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
    subfolder: str | None
        The subfolder that the file is contained within
    Returns
    -------
    pd.DataFrame
        The Raman spectrum dataset as a dataframe
    """

    folder = get_level_path(level)

    if subfolder != None:
        folder = folder / subfolder

    # Try exact names first, then known project aliases such as mettler -> mettler_toledo.csv.
    candidates = [
        folder / name,
        folder / f"{name}.csv",
        folder / f"{name}.parquet",
    ]

    if name in DATASET_NAME_ALIASES:
        candidates.append(folder / f"{DATASET_NAME_ALIASES[name]}.csv")
        candidates.append(folder / f"{DATASET_NAME_ALIASES[name]}.parquet")

    for file_path in candidates:
        if file_path.exists():
            return pd.read_csv(file_path,index_col=False, header=header)
    
    raise FileNotFoundError(name)

def read_raman_file_from_path(file_path: Path, header: int | None = 0) -> pd.DataFrame:
    """
    Read a Raman spectrum dataset from a file path
    
    Parameters
    ----------
    file_path: Path
        The Path of the raman file to read from
    Returns
    -------
    pd.DataFrame
        The Raman spectrum dataset as a dataframe
    """

    if file_path.exists():
        return pd.read_csv(file_path,index_col=False, header=header)
    
    raise FileNotFoundError(file_path)

def write_raman_file(df: pd.DataFrame, level: str, output_filename: str, output_folder: str = None) -> None:
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
    output_folder: str, Optional
        The folder within the specified level folder to save the dataset to. Blank means no subfolder
    """
    folder = get_level_path(level)
    if output_folder is not None:
        folder = folder / output_folder
        if not os.path.exists(folder):
            os.mkdir(folder)

    if output_filename.lower().strip().endswith('.csv'):
        df.to_csv(folder / output_filename, index=False)
    elif output_filename.lower().strip().endswith('.parquet'):
        df.to_parquet(folder / output_filename, index=False)
    else:
        raise ValueError(f'Unsupported or missing filetype: {output_filename}')

def read_raman_files(names: Iterable[str],level: str) -> dict[str, pd.DataFrame]:
    """Read several Raman datasets from the same data level."""
    return {
        name: read_raman_file(name=name, level=level)
        for name in names
    }

def read_config_file(config_type: str, config_name: str) -> dict:

    folder = get_configs_path(config_type)

    if not os.path.exists(folder/config_name):
        raise FileNotFoundError(f'{folder/config_name} does not exist')

    with open(folder/config_name) as f:
        config = yaml.safe_load(f)

    return config

def get_preprocessing_config_names() -> list[str]:
    print(PREPROCESSING_CONFIG_FOLDER)

    names = [p.name for p in PREPROCESSING_CONFIG_FOLDER.iterdir()]

    return names