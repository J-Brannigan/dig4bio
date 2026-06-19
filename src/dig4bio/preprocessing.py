import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
from dig4bio.constants import FINGERPRINT_GRID

def interpolate_spectra_to_grid(spectra: np.ndarray, old_wavenumbers: np.ndarray, new_wavenumbers: np.ndarray = FINGERPRINT_GRID) -> np.ndarray:
    """Linearly interpolate spectra onto a common wavenumber grid."""

    f = make_interp_spline(old_wavenumbers,spectra,k=1,axis=1,check_finite=True)

    return f(new_wavenumbers,extrapolate=False)