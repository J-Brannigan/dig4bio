"""Orchestration functions for project data workflows."""

from matplotlib import pyplot as plt
import numpy as np

from dig4bio.data_cleaning import (
    clean_test_samples_data,
    clean_transfer_plate_data,
    clean_source_device_data
)
from dig4bio.preprocessing import align_spectral_dfs_to_common_grid
from dig4bio.io import read_raman_file, read_raman_files, write_raman_file, read_config_file
from dig4bio.visualisation import generate_samples_plot
from dig4bio.datasets import combine_source_datasets
from dig4bio.paths import FIGURES_EDA_FOLDER
from dig4bio.constants import ALL_DEVICE_NAMES, SOURCE_DEVICE_NAMES
from dig4bio.config import get_input_params, get_interpolation_params, get_output_params, get_wavenumber_grid_from_config, get_experiment_params

def make_interim_transfer_plate(output_filename: str = 'transfer_plate.csv') -> None:
    """Create and save the cleaned interim transfer plate dataset."""
    
    raw_df = read_raman_file(
        name="transfer_plate",
        level="raw",
    )
    
    interim_df = clean_transfer_plate_data(raw_df)

    write_raman_file(
        df=interim_df,
        level='interim',
        output_filename=output_filename,
    )

def make_interim_test_samples(output_filename: str = "96_samples.csv") -> None:
    """Create and save the cleaned interim 96-sample dataset."""
    raw_df = read_raman_file(
        name="96_samples",
        level="raw",
        header=None,
    )

    interim_df = clean_test_samples_data(raw_df)

    write_raman_file(
        df=interim_df,
        level="interim",
        output_filename=output_filename,
    )

def make_interim_source_devices() -> None:
    """Create and save the interim source-device datasets."""
    for device_name in SOURCE_DEVICE_NAMES:
        raw_df = read_raman_file(
            name=device_name,
            level="raw",
        )

        interim_df = clean_source_device_data(raw_df)

        write_raman_file(
            df=interim_df,
            level="interim",
            output_filename=f"{device_name}.csv",
        )

def make_processed_source_dataset(config_name: str) -> None:
    """Create and save the combined source-device dataset."""

    config = read_config_file('preprocessing',config_name)

    # Get parameters from config YAML file
    new_wavenumber_grid = get_wavenumber_grid_from_config(config)
    interpolation_params = get_interpolation_params(config)
    input_params = get_input_params(config)
    output_params = get_output_params(config)
    add_device_column = config.get("combine", {}).get("add_device_column", True)

    source_device_dfs = read_raman_files(**input_params)

    aligned_dfs = align_spectral_dfs_to_common_grid(
        source_datasets=source_device_dfs,
        new_wavenumbers=new_wavenumber_grid,
        **interpolation_params
    )
    
    combined_df = combine_source_datasets(
        aligned_dfs,
        add_device_column=add_device_column
    )

    write_raman_file(
        df = combined_df,
        **output_params
    )

def make_sample_spectra_plot(output_filename: str = "sample_spectra_by_dataset.png") -> None:
    """Create and save the EDA sample-spectra figure."""
    
    interim_dfs = read_raman_files(ALL_DEVICE_NAMES,level="interim")

    fig = generate_samples_plot(dfs=interim_dfs)

    output_path = FIGURES_EDA_FOLDER / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, dpi=400, bbox_inches="tight")
    plt.close(fig)

def make_all_processed_datasets(preprocessing_config_name: str) -> None:
    """Create the processed source datasets ready for modelling"""
    make_processed_source_dataset(config_name=preprocessing_config_name)

def make_all_interim_datasets() -> None:
    """Create all interim datasets from the raw competition files."""
    make_interim_transfer_plate()
    make_interim_test_samples()
    make_interim_source_devices()

def prepare_all_data(preprocessing_config_name: str) -> None:
    """Prepare all project datasets for modelling."""
    make_all_interim_datasets()
    make_all_processed_datasets(preprocessing_config_name=preprocessing_config_name)

def make_all_eda_figures() -> None:
    """Create all EDA figures that depend on interim datasets."""
    make_sample_spectra_plot()