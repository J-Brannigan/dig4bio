import pandas as pd
import numpy as np

def clean_transfer_plate_data(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean the raw labelled transfer-plate dataframe.

    Parameters
    ----------
    raw_df:
        Raw transfer-plate data as loaded from the competition file.

    Returns
    -------
    pd.DataFrame
        Cleaned transfer-plate data with sample identifiers, wavenumber
        columns and concentration labels correctly assigned.
    """
    spectral_columns = raw_df.columns[1:-4].tolist()

    cleaned_df = (
        raw_df.copy()
        .pipe(
            _remove_brackets_from_spectral_vals,
            spectral_columns=spectral_columns,
        )
        .pipe(_label_df_columns)
        .pipe(_strip_column_whitespace, column_name="sample")
        .pipe(_forward_fill_column, column_name="sample")
        .pipe(_reassign_transfer_sample_rows)
    )

    return cleaned_df

def clean_test_samples_data(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean the raw unlabelled 96-sample dataframe."""
    spectral_columns = raw_df.columns[1:].tolist()

    cleaned_df = (
        raw_df.copy()
        .pipe(
            _remove_brackets_from_spectral_vals,
            spectral_columns=spectral_columns,
        )
        .pipe(_label_df_columns, has_label_cols=False)
        .pipe(_strip_column_whitespace, column_name="sample")
        .pipe(_forward_fill_column, column_name="sample")
    )

    return cleaned_df

def clean_source_device_data(
    raw_df: pd.DataFrame
) -> pd.DataFrame:
    """Validate and standardise a raw source-device dataset."""
    cleaned_df = raw_df.copy()

    return cleaned_df

def _reassign_transfer_sample_rows(df: pd.DataFrame) -> pd.DataFrame:
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

def _remove_brackets_from_spectral_vals(df: pd.DataFrame, spectral_columns: list[str]) -> pd.DataFrame:
    """Remove raw-file square bracket artifacts from spectral values."""
    df[spectral_columns] = df[spectral_columns].replace(r'[\[\]]','',regex=True)
    return df

def _label_df_columns(df: pd.DataFrame, has_label_cols: bool = True) -> pd.DataFrame:
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

def _strip_column_whitespace(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Strip leading and trailing whitespace from identifier columns."""
    df[column_name] = df[column_name].str.strip()   
    return df

def _forward_fill_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Forward-fill repeated sample identifiers.

    The transfer and test plate files store two spectra per sample, but the
    second row often leaves the sample name blank. Forward filling assigns the
    repeated spectrum back to the same sample.
    """
    df[column_name] = df[column_name].ffill(axis=0)
    return df


def rename_df_column(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    print(mapping)

    output_df = df.copy()
    output_df = output_df.rename(columns=mapping)

    return output_df
