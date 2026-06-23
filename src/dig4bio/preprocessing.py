import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

from dig4bio.utils import get_interim_spectral_cols

def build_wavenumber_grid(wavenumber_start: float = 300, wavenumber_end: float = 1800, wavenumber_step: float = 1) -> np.ndarray:
    """Build the grid of wavenumbers. Assume fingerprint region (300-1800)cm^-1 with single cm^-1 steps unless other params given"""
    return np.arange(wavenumber_start,wavenumber_end+1,wavenumber_step)

def interpolate_spectra_to_grid(spectra: np.ndarray, old_wavenumbers: np.ndarray, new_wavenumbers: np.ndarray | None = None) -> np.ndarray:
    """Linearly interpolate spectra onto a common wavenumber grid."""

    if new_wavenumbers is None:
        new_wavenumbers = build_wavenumber_grid()

    f = make_interp_spline(old_wavenumbers,spectra,k=1,axis=1,check_finite=True)

    return f(new_wavenumbers,extrapolate=False)


def align_spectral_dfs_to_common_grid(source_datasets: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Interpolate dataframe wavenumbers onto common wavenumber grid

    Parameters
    ----------
    source_datasets: dict[str, pd.DataFrame]
        Dictionary of the names and dataframes of each dataset

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary of the names and dataframes of each dataset aligned to a common grid
    """


    aligned_dfs = {}

    fingerprint_wavenumber_grid = build_wavenumber_grid()

    for device_name, df in source_datasets.items():

        df_copy = df.copy()

        # The spectral columns of each dataset are in different places in the df
        spectral_columns = get_interim_spectral_cols(device_name, df_copy)

        spectra_df = df_copy[spectral_columns]
        labels_df = df_copy.drop(columns = spectral_columns)

        old_wavenumbers = np.array(spectral_columns)

        interpolated_spectra = interpolate_spectra_to_grid(spectra= spectra_df, old_wavenumbers=old_wavenumbers, new_wavenumbers=fingerprint_wavenumber_grid)

        interpolated_df = pd.DataFrame(interpolated_spectra, columns = fingerprint_wavenumber_grid.astype(str), index=df.index)
        interpolated_df = pd.concat([interpolated_df,labels_df],axis=1)

        aligned_dfs[device_name] = interpolated_df

    return aligned_dfs