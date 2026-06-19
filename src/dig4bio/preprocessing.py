import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from dig4bio.constants import FINGERPRINT_GRID

def interpolate_spectra_to_grid(spectra: np.ndarray, old_wavenumbers: np.ndarray, new_wavenumbers: np.ndarray = FINGERPRINT_GRID) -> np.ndarray:
    """Interpolate spectra from one wavenumber grid to another."""
    f = interp1d(old_wavenumbers, spectra, axis=1, kind="linear", bounds_error=False, fill_value=np.nan)
    return f(new_wavenumbers)