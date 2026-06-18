import pandas as pd
import numpy as np

def reassign_transfer_sample_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Attach transfer plate concentration labels to each spectrum row.

    In the raw transfer plate file, spectra and concentration labels are stored
    in different parts of the same dataframe. The spectrum rows identify samples
    by name, while the label table stores those names under `Analyte concentration`.
    This merge copies the known concentrations onto each repeated spectrum row.
    
    Parameters
    ----------
    df: pd.DataFrame
        Raw transfer plate dataframe after sample names and spectral columns
        have been cleaned.
    
    Returns
    -------
    pd.DataFrame
        Cleaned transfer plate dataframe where each row contains one spectrum
        and its corresponding analyte concentrations.
    """
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
    """Remove raw-file square bracket artifacts from spectral values."""
    df[spectral_columns] = df[spectral_columns].replace(r'[\[\]]','',regex=True)
    return df

def label_df_columns(df: pd.DataFrame, has_label_cols: bool = True) -> pd.DataFrame:
    """
    Assign sample, wavenumber, and optional label column names.

    The target-domain raw files do not provide clean spectral column names. They
    are known to contain 2,048 spectral measurements from 65 to 3,350 cm^-1, so
    this function reconstructs the wavenumber labels from that metadata.
    """
    start_wavenumber = 65
    end_wavenumber = 3350
    wavenumber_count = 2048

    sample_col = ['sample']
    spectral_cols = np.linspace(start_wavenumber,end_wavenumber,wavenumber_count).round(2).tolist()
    if has_label_cols:
        label_cols = df.columns[-4:].tolist()
        df.columns = sample_col + spectral_cols + label_cols
    else:
        df.columns = sample_col + spectral_cols

    return df

def strip_column_whitespace(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Strip leading and trailing whitespace from identifier columns."""
    df[column_name] = df[column_name].str.strip()   
    return df

def forward_fill_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Forward-fill repeated sample identifiers.

    The transfer and test plate files store two spectra per sample, but the
    second row often leaves the sample name blank. Forward filling assigns the
    repeated spectrum back to the same sample.
    """
    df[column_name] = df[column_name].ffill(axis=0)
    return df
