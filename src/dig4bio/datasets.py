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

def generate_transfer_dataframes(df, test_device: str, fold_idx: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """From a source dataframe of raman spectra, create a dataframe to train on, a dataframe to simulate model calibration, and a dataframe to test on.
    
    The test and calibration dataframes will contain all data only from the 'test_device' to simulate a newly added device.

    The train and calibration dataframes will contain all data not from the 'fold_idx' to simulate a newly seen sample. (Each sample does not span more than one fold_idx)
    """

    source_df = df[df['device'] != test_device]
    transfer_test_df = df[df['device'] == test_device]

    source_train = source_df[source_df['fold_idx'] != fold_idx]
    target_calibration = transfer_test_df[transfer_test_df['fold_idx'] != fold_idx]
    target_test = transfer_test_df[transfer_test_df['fold_idx'] == fold_idx]
    
    return source_train, target_calibration, target_test
