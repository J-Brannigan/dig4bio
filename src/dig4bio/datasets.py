from dig4bio.io import read_raman_file
from dig4bio.data_cleaning import (
    remove_brackets_from_spectral_vals,
    label_df_columns,
    strip_column_whitespace,
    forward_fill_column, 
    reassign_transfer_sample_rows
    )
from dig4bio.constants import SOURCE_DEVICE_NAMES, ALL_DEVICE_NAMES


def make_interim_transfer_plate_data():
    """Load and clean the raw labelled transfer plate dataset."""

    raw_transfer_df = read_raman_file(name='transfer_plate',level='raw')

    # The raw transfer plate has a sample column, spectral columns, and label
    # columns. The spectral values arrive with square brackets and unnamed
    # wavenumber columns, so this step normalises the structure.
    cleaned_transfer_df = (
        raw_transfer_df
        .pipe(remove_brackets_from_spectral_vals, spectral_columns = raw_transfer_df.columns[1:-4].tolist())
        .pipe(label_df_columns)
        .pipe(strip_column_whitespace, column_name = 'sample')
        .pipe(forward_fill_column, column_name = 'sample')
    )

    # Concentration labels are stored separately from the repeated spectral
    # rows in the raw file, so attach them to each cleaned spectrum row.
    cleaned_transfer_df = reassign_transfer_sample_rows(cleaned_transfer_df)
    
    return cleaned_transfer_df


def make_interim_test_samples_data():
    """Load and clean the raw unlabelled 96-sample test dataset."""

    # The test file has no header row and no concentration labels.
    raw_test_samples_df = read_raman_file(name='96_samples',level='raw',header=None)

    # Test spectra have the same bracketed-value/sample-name quirks as the
    # transfer plate, but only contain sample identifiers and spectral columns.
    cleaned_test_samples_df = (
         raw_test_samples_df
         .pipe(remove_brackets_from_spectral_vals,spectral_columns = raw_test_samples_df.columns[1:].tolist())
         .pipe(label_df_columns, has_label_cols = False)
         .pipe(strip_column_whitespace, column_name = 'sample')
         .pipe(forward_fill_column, column_name = 'sample')
     )

    return cleaned_test_samples_df


def make_interim_8_devices_data():
    """Load the raw source-device datasets into a dataframe dictionary."""

    # The source-device files are already structurally clean enough for the
    # interim layer, so this step mainly standardises loading and naming.
    raw_by_model =  {dataset: read_raman_file(name=dataset,level='raw') for dataset in SOURCE_DEVICE_NAMES}

    return raw_by_model


def load_interim_datasets():
    """Load all interim datasets used by downstream EDA and modelling stages."""

    interim_dfs = {dataset: read_raman_file(name=dataset, level='interim') for dataset in ALL_DEVICE_NAMES}

    return interim_dfs
