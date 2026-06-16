"""Pipeline orchestration for project data workflows."""

from dig4bio.datasets import make_interim_8_devices_data, make_interim_test_samples_data, make_interim_transfer_plate_data
from dig4bio.io import write_raman_file


def make_interim_transfer_plate(output_filename: str = 'transfer_plate.csv') -> None:
    interim_df = make_interim_transfer_plate_data()
    write_raman_file(
        df=interim_df,
        level='interim',
        output_filename=output_filename,
    )


def make_interim_test_samples(output_filename: str = '96_samples.csv') -> None:
    interim_df = make_interim_test_samples_data()
    write_raman_file(
        df=interim_df,
        level='interim',
        output_filename=output_filename,
    )


def make_interim_8_devices() -> None:
    interim_dfs = make_interim_8_devices_data()

    for model, df in interim_dfs.items():
        write_raman_file(
            df=df,
            level='interim',
            output_filename=f'{model}.csv',
        )


def make_all_interim_datasets() -> None:
    make_interim_transfer_plate()
    make_interim_test_samples()
    make_interim_8_devices()
