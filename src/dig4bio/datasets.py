import pandas as pd

def combine_source_datasets(source_datasets: dict[str, pd.DataFrame], add_device_column: bool) -> pd.DataFrame:
    """Append the rows of each dataset in the source dataset dictionary together and label each device name
    
    This function assumes the datasets share the same columns
    """

    labelled_dfs=[]

    for device_name, df in source_datasets.items():
        labelled_df = df.copy()
        if add_device_column:
            labelled_df['device'] = device_name
        labelled_dfs.append(labelled_df)

    combined_df = pd.concat(labelled_dfs,axis=0,ignore_index=True)

    return combined_df

def get_device_fold_df(df, test_device: str, fold_idx: int, category: str, train_on_target: bool = False) -> pd.DataFrame:
    """From a source DataFrame of raman spectra, create a dataframe to train on, a DataFrame to simulate model calibration, and a DataFrame to test on.
    
    The test and calibration DataFrames will contain all data only from the 'test_device' to simulate a newly added device.

    The train and calibration DataFrames will contain all data not from the 'fold_idx' to simulate a newly seen sample. (Each sample does not span more than one fold_idx)
    """

    if train_on_target:
        source_df = df[df['device'] == test_device]
    else:
        source_df = df[df['device'] != test_device]

    transfer_test_df = df[df['device'] == test_device]

    if category == 'train':
        output_df = source_df[source_df['fold_idx'] != fold_idx]
    elif category == 'calibration':
        output_df = transfer_test_df[transfer_test_df['fold_idx'] != fold_idx]
    elif category == 'test':
        output_df =  transfer_test_df[transfer_test_df['fold_idx'] == fold_idx]
    else:
        raise ValueError(f'Fold DataFrame category must be one of "train", "calibration", or "test". Provided: {category}')
    
    return output_df

def get_fold_df(df, fold_idx: int, category: str) -> pd.DataFrame:
    """From a source DataFrame of raman spectra split by fold_idx, create a dataframe to train on, and a DataFrame to test on.
    
    The test DataFrame will contain all data only from the 'test_device' to simulate a newly added device.

    The train DataFrame will contain all data not from the 'fold_idx' to simulate a newly seen sample. (Each sample does not span more than one fold_idx).
    """

    if category == 'train':
        output_df = df[df['fold_idx'] != fold_idx]
    elif category == 'test':
        output_df =  df[df['fold_idx'] == fold_idx]
    else:
        raise ValueError(f'Fold DataFrame category must be "train" or "test". Provided: {category}')
    
    return output_df


def get_interim_spectral_cols(device: str, df: pd.DataFrame) -> list[str]:
    """Return spectral column names for an interim dataset.

    Interim source-device, transfer plate, and test datasets have different
    metadata/label/spectral columns, so the columns occupy different slices.
    """
    if device == 'transfer_plate':
        spectral_cols = df.columns[1:-3]
    elif device == '96_samples':
        spectral_cols = df.columns[1:]
    else:
        spectral_cols = df.columns[:-5]

    return spectral_cols.tolist()
