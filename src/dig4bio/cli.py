"""Command-line entry points for project workflows."""

import argparse

from dig4bio.datasets import make_interim_transfer_plate_data, make_interim_test_samples_data, make_interim_8_devices_data
from dig4bio.io import write_raman_file

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

    interim_df = make_interim_transfer_plate_data()
    write_raman_file(df=interim_df, level='interim', output_filename=args.output_filename)

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

    interim_df = make_interim_test_samples_data()
    write_raman_file(df=interim_df, level='interim', output_filename=args.output_filename)

def make_interim_8_devices_command() -> None:

    parser = argparse.ArgumentParser(
        description="Create the interim 8 device datasets from the raw 8 devices data."
    )
    
    args = parser.parse_args()

    interim_dfs = make_interim_8_devices_data()

    for model, df in interim_dfs.items():
        write_raman_file(df=df, level='interim', output_filename= f'{model}.csv')

def make_all_interim_command() -> None:

    parser = argparse.ArgumentParser(
        description="Create all interim datasets from the raw data."
    )
    
    args = parser.parse_args()

    make_interim_transfer_plate_command()
    make_interim_test_samples_command()
    make_interim_8_devices_command()