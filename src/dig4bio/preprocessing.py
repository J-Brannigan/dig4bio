import numpy as np
from scipy.interpolate import make_interp_spline

def build_wavenumber_grid(wavenumber_start: float = 300, wavenumber_end: float = 1800, wavenumber_step: float = 1) -> np.ndarray:
    """Build the grid of wavenumbers. Assume fingerprint region (300-1800)cm^-1 with single cm^-1 steps unless other params given"""
    return np.arange(wavenumber_start,wavenumber_end,wavenumber_step)

def interpolate_spectra_to_grid(spectra: np.ndarray, old_wavenumbers: np.ndarray, new_wavenumbers: np.ndarray | None = None) -> np.ndarray:
    """Linearly interpolate spectra onto a common wavenumber grid."""

    if new_wavenumbers is None:
        new_wavenumbers = build_wavenumber_grid()

    f = make_interp_spline(old_wavenumbers,spectra,k=1,axis=1,check_finite=True)

    return f(new_wavenumbers,extrapolate=False)