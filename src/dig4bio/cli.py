"""Command-line entry points for project workflows."""

import argparse

from dig4bio.pipelines import (
    make_all_interim_datasets,
    make_interim_8_devices,
    make_interim_test_samples,
    make_interim_transfer_plate,
)

def make_interim_transfer_plate_command() -> None:

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

    make_interim_transfer_plate(output_filename=args.output_filename)

def make_interim_test_samples_command() -> None:

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

    make_interim_test_samples(output_filename=args.output_filename)

def make_interim_8_devices_command() -> None:

    parser = argparse.ArgumentParser(
        description="Create the interim 8 device datasets from the raw 8 devices data."
    )
    
    parser.parse_args()

    make_interim_8_devices()

def make_all_interim_command() -> None:

    parser = argparse.ArgumentParser(
        description="Create all interim datasets from the raw data."
    )
    
    parser.parse_args()

    make_all_interim_datasets()
