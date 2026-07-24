import numpy as np
from dig4bio.constants import FINGERPRINT_GRID, SOURCE_DEVICE_NAMES
from dig4bio.preprocessing import build_wavenumber_grid

def get_wavenumber_grid_from_config(config: dict) -> np.ndarray:
    grid_config = config.get("wavenumber_grid", {})

    return build_wavenumber_grid(
        wavenumber_start=grid_config.get("start", FINGERPRINT_GRID[0]),
        wavenumber_end=grid_config.get("end", FINGERPRINT_GRID[-1]),
        wavenumber_step=grid_config.get("step", np.diff(FINGERPRINT_GRID)[0]),
    )

def get_interpolation_params(config: dict) -> dict:
    interpolation_config = config.get("interpolation", {})

    return {
        "interpolation_method": interpolation_config.get("method", "linear"),
        "extrapolate": interpolation_config.get("extrapolate", False),
    }

def get_output_params(config: dict) -> dict:
    output_config = config.get("outputs", {})

    return {
        "level": output_config.get("level", "processed"),
        "output_folder": output_config.get("folder", "source_grid_fingerprint_linear"),
        "output_filename": output_config.get("file", "source_datasets.csv"),
    }

def get_input_params(config: dict) -> dict:
    input_config = config.get("inputs", {})

    input_datasets = input_config.get("datasets")

    if input_datasets is None:
        raise ValueError("Config must define inputs.datasets")

    if input_datasets == "source_devices":
        input_datasets = SOURCE_DEVICE_NAMES

    return {
        "level": input_config.get("level", "interim"),
        "names": input_datasets
    }

def get_experiment_params(cofig: dict) -> dict:

    
    return 