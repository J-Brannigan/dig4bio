from dig4bio.io import read_raman_file
from dig4bio.data_cleaning import (
    remove_brackets_from_spectral_vals,
    label_transfer_plate_cols,
    strip_column_whitespace,
    forward_fill_column, 
    reassign_transfer_sample_rows
    )

def make_interim_transfer_plate_data():

    raw_transfer_df = read_raman_file(name='transfer_plate',level='raw')

    clean_transfer_df = (
        raw_transfer_df
        .pipe(remove_brackets_from_spectral_vals, spectral_columns = raw_transfer_df.columns[1:-4].tolist())
        .pipe(label_transfer_plate_cols)
        .pipe(strip_column_whitespace, column_name = 'sample')
        .pipe(forward_fill_column, column_name = 'sample')
    )

    clean_transfer_df = reassign_transfer_sample_rows(clean_transfer_df)
    
    return clean_transfer_df