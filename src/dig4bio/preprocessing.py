import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

from dig4bio.utils import get_interim_spectral_cols
from dig4bio.constants import FINGERPRINT_GRID

def build_wavenumber_grid(wavenumber_start: float = 300, wavenumber_end: float = 1800, wavenumber_step: float = 1) -> np.ndarray:
    """Build the grid of wavenumbers. Assume fingerprint region (300-1800)cm^-1 with single cm^-1 steps unless other params given"""
    return np.arange(wavenumber_start,wavenumber_end+1,wavenumber_step)

def interpolate_spectra_to_grid(
        spectra: np.ndarray,
        old_wavenumbers: np.ndarray,
        new_wavenumbers: np.ndarray,
        interpolation_method: str = 'linear',
        extrapolate: bool = False
    ) -> np.ndarray:
    """Interpolate spectra onto a common wavenumber grid."""

    if interpolation_method == 'linear':
        b_spline_degree=1
    elif interpolation_method == 'cubic':
        b_spline_degree=3
    else:
        raise ValueError(f'interpolation_method value not supported: {interpolation_method}')
    
    # Produces a B-Spline object
    f = make_interp_spline(
        old_wavenumbers,
        spectra,
        k=b_spline_degree,
        axis=1,
        check_finite=True
    )

    if not extrapolate:
        if new_wavenumbers.min() < old_wavenumbers.min():
            raise ValueError("Target grid starts before source wavenumber range and extrapolate is set to False.")

        if new_wavenumbers.max() > old_wavenumbers.max():
            raise ValueError("Target grid ends after source wavenumber range and extrapolate is set to False.")
    
    return f(new_wavenumbers,extrapolate=extrapolate)


def align_spectral_dfs_to_common_grid(
        source_datasets: dict[str, pd.DataFrame],
        new_wavenumbers: np.ndarray,
        interpolation_method: str,
        extrapolate: bool
    ) -> dict[str, pd.DataFrame]:
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

    aligned_dfs={}

    for device_name, df in source_datasets.items():

        df_copy = df.copy()

        # The spectral columns of each dataset are in different places in the df
        spectral_columns = get_interim_spectral_cols(device_name, df_copy)

        spectra_df = df_copy[spectral_columns]
        labels_df = df_copy.drop(columns = spectral_columns)

        old_wavenumbers = np.array(spectral_columns,dtype=float)

        # Create new spectra over the new wavenumber grid from original points
        interpolated_spectra = interpolate_spectra_to_grid(
            spectra= spectra_df,
            old_wavenumbers=old_wavenumbers,
            new_wavenumbers=new_wavenumbers,
            interpolation_method = interpolation_method,
            extrapolate = extrapolate
            )

        # Label columns with new wavenumber values
        interpolated_df = pd.DataFrame(interpolated_spectra, columns = new_wavenumbers.astype(str), index=df.index)
        
        # Add original row label columns to newly interpolated values
        interpolated_df = pd.concat([interpolated_df,labels_df],axis=1)

        aligned_dfs[device_name] = interpolated_df

    return aligned_dfs