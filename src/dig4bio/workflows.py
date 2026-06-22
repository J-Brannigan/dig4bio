"""Orchestration functions for project data workflows."""

from matplotlib import pyplot as plt

from dig4bio.data_cleaning import (
    clean_test_samples_data,
    clean_transfer_plate_data,
    clean_source_device_data
)
from dig4bio.io import read_raman_file, read_raman_files, write_raman_file
from dig4bio.visualisation import generate_samples_plot
from dig4bio.paths import FIGURES_EDA_FOLDER
from dig4bio.constants import ALL_DEVICE_NAMES, SOURCE_DEVICE_NAMES

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

def make_sample_spectra_plot(output_filename: str = "sample_spectra_by_dataset.png") -> None:
    """Create and save the EDA sample-spectra figure."""
    
    interim_dfs = read_raman_files(ALL_DEVICE_NAMES,level="interim")

    fig = generate_samples_plot(dfs=interim_dfs)

    output_path = FIGURES_EDA_FOLDER / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, dpi=400, bbox_inches="tight")
    plt.close(fig)

def make_all_interim_datasets() -> None:
    """Create all interim datasets from the raw competition files."""
    make_interim_transfer_plate()
    make_interim_test_samples()
    make_interim_source_devices()

def make_all_eda_figures() -> None:
    """Create all EDA figures that depend on interim datasets."""
    make_sample_spectra_plot()
