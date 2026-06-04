import pandas as pd
import numpy as np
from dig4bio.io import read_raman_file

def reassign_transfer_sample_rows(df: pd.DataFrame) -> pd.DataFrame:

    transfer_spectra_df = df[df.columns[:-4]]
    transfer_samples_df = df[df.columns[-4:]]

    clean_transfer_df = pd.merge(
        left = transfer_spectra_df,
        right=transfer_samples_df, 
        left_on='sample',
        right_on='Analyte concentration',
        how='inner',
        copy=False
        ).drop('Analyte concentration',axis=1)

    return clean_transfer_df

def remove_brackets_from_spectral_vals(df: pd.DataFrame, spectral_columns: list[str]) -> pd.DataFrame:
    df[spectral_columns] = df[spectral_columns].replace(r'[\[\]]','',regex=True)
    return df

def label_transfer_plate_cols(df: pd.DataFrame) -> pd.DataFrame:
    start_wavenumber = 65
    end_wavenumber = 3350
    wavenumber_count = 2048

    sample_col = ['sample']
    spectral_cols = np.linspace(start_wavenumber,end_wavenumber,wavenumber_count).round(2).tolist()
    label_cols = df.columns[-4:].tolist()

    df.columns = sample_col + spectral_cols + label_cols

    return df

def strip_column_whitespace(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].str.strip()   
    return df

def forward_fill_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].ffill(axis=0)
    return df