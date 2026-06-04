"""Command-line entry points for project workflows."""

import argparse

from dig4bio.datasets import make_interim_transfer_plate_data
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