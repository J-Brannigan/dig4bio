"""Command-line entry points for project workflows."""

import argparse

from dig4bio.pipelines import (
    make_all_interim_datasets,
    make_interim_8_devices,
    make_interim_test_samples,
    make_interim_transfer_plate,
    make_all_eda_figures,
)


def make_interim_transfer_plate_command() -> None:
    """CLI wrapper for creating the interim transfer plate dataset."""

    parser = argparse.ArgumentParser(
        description="Create the interim transfer plate dataset from the raw transfer plate data."
    )

    parser.add_argument(
        '--output_filename',
        type=str,
        default='transfer_plate.csv',
        help="Filename to save the interim transfer plate dataset."
    )

    args = parser.parse_args()

    # CLI functions should only parse arguments and delegate to pipeline code.
    make_interim_transfer_plate(output_filename=args.output_filename)


def make_interim_test_samples_command() -> None:
    """CLI wrapper for creating the interim 96-sample test dataset."""

    parser = argparse.ArgumentParser(
        description="Create the interim test samples dataset from the raw test samples data."
    )

    parser.add_argument(
        '--output_filename',
        type=str,
        default='96_samples.csv',
        help="Filename to save the interim test samples dataset."
    )

    args = parser.parse_args()

    # CLI functions should only parse arguments and delegate to pipeline code.
    make_interim_test_samples(output_filename=args.output_filename)


def make_interim_8_devices_command() -> None:
    """CLI wrapper for creating all interim source-device datasets."""

    parser = argparse.ArgumentParser(
        description="Create the interim 8 device datasets from the raw 8 devices data."
    )
    
    parser.parse_args()

    # No command arguments are needed yet; parse_args still gives --help support.
    make_interim_8_devices()


def make_all_interim_command() -> None:
    """CLI wrapper for creating every interim dataset."""

    parser = argparse.ArgumentParser(
        description="Create all interim datasets from the raw data."
    )
    
    parser.parse_args()

    # Delegate to the pipeline instead of calling other CLI functions. This
    # avoids nested argparse calls when running the full data-cleaning stage.
    make_all_interim_datasets()


def make_all_eda_figures_command() -> None:
    """CLI wrapper for creating all EDA figure outputs."""

    parser = argparse.ArgumentParser(
        description="Create all EDA figures from the interim data."
    )
    
    parser.parse_args()

    # This pipeline expects interim datasets to exist already.
    make_all_eda_figures()
