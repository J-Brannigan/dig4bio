import pandas as pd

def combine_source_datasets(source_datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Append the rows of each dataset in the source dataset dictionary together and label each device name
    
    This function assumes the datasets share the same columns
    """

    labelled_dfs=[]

    for device_name, df in source_datasets.items():
        labelled_df = df.copy()
        labelled_df['device'] = device_name
        labelled_dfs.append(labelled_df)

    combined_df = pd.concat(labelled_dfs,axis=0,ignore_index=True)

    return combined_df
