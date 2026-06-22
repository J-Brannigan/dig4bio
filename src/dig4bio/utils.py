import pandas as pd


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