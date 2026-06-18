"""Pipeline orchestration for project data workflows."""

from dig4bio.datasets import (
    make_interim_8_devices_data,
    make_interim_test_samples_data,
    make_interim_transfer_plate_data,
    load_interim_datasets,
)
from dig4bio.io import write_raman_file
from dig4bio.visualisation import generate_samples_plot
from dig4bio.paths import FIGURES_EDA_FOLDER

def make_interim_transfer_plate(output_filename: str = 'transfer_plate.csv') -> None:
    """Create and save the cleaned interim transfer plate dataset."""
    interim_df = make_interim_transfer_plate_data()

    write_raman_file(
        df=interim_df,
        level='interim',
        output_filename=output_filename,
    )


def make_interim_test_samples(output_filename: str = '96_samples.csv') -> None:
    """Create and save the cleaned interim 96-sample test dataset."""
    interim_df = make_interim_test_samples_data()

    write_raman_file(
        df=interim_df,
        level='interim',
        output_filename=output_filename,
    )


def make_interim_8_devices() -> None:
    """Create and save one interim dataset for each source device."""
    interim_dfs = make_interim_8_devices_data()

    # Keep one file per source device so later stages can either load devices
    # separately or combine them with an explicit device label.
    for model, df in interim_dfs.items():
        write_raman_file(
            df=df,
            level='interim',
            output_filename=f'{model}.csv',
        )

def make_sample_spectra_plot(output_filename: str = 'sample_spectra_by_dataset.png') -> None:
    """Create and save the EDA sample spectra figure from interim datasets."""

    # This stage depends on the interim datasets already existing.
    # Run 'clean-all-data' first if any interim files are missing or stale.
    interim_dfs = load_interim_datasets()

    # Figure construction lives in visualisation.py. This pipeline owns loading
    # inputs and writing the generated artifact to disk.
    fig = generate_samples_plot(dfs=interim_dfs)

    output_path = FIGURES_EDA_FOLDER / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, dpi=400, bbox_inches="tight")

def make_all_interim_datasets() -> None:
    """Create all interim datasets from the raw competition files."""
    make_interim_transfer_plate()
    make_interim_test_samples()
    make_interim_8_devices()

def make_all_eda_figures() -> None:
    """Create all EDA figures that depend on interim datasets."""
    make_sample_spectra_plot()
