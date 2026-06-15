from dig4bio.io import read_raman_file
from dig4bio.data_cleaning import (
    remove_brackets_from_spectral_vals,
    label_df_columns,
    strip_column_whitespace,
    forward_fill_column, 
    reassign_transfer_sample_rows
    )

def make_interim_transfer_plate_data():

    raw_transfer_df = read_raman_file(name='transfer_plate',level='raw')

    cleaned_transfer_df = (
        raw_transfer_df
        .pipe(remove_brackets_from_spectral_vals, spectral_columns = raw_transfer_df.columns[1:-4].tolist())
        .pipe(label_df_columns)
        .pipe(strip_column_whitespace, column_name = 'sample')
        .pipe(forward_fill_column, column_name = 'sample')
    )

    cleaned_transfer_df = reassign_transfer_sample_rows(cleaned_transfer_df)
    
    return cleaned_transfer_df

def make_test_samples_data():

    raw_test_samples_df = read_raman_file(name='96_samples',level='raw',header=None)

    cleaned_test_samples_df = (
         raw_test_samples_df
         .pipe(remove_brackets_from_spectral_vals,spectral_columns = raw_test_samples_df.columns[1:].tolist())
         .pipe(label_df_columns, has_label_cols = False)
         .pipe(strip_column_whitespace, column_name = 'sample')
         .pipe(forward_fill_column, column_name = 'sample')
     )

    return cleaned_test_samples_df