import pandas as pd
from dig4bio.datasets import generate_transfer_dataframes
from dig4bio.evaluation import get_error_function
import numpy as np

def augmented_cross_validate(
        source_df: pd.DataFrame,
        wavenumber_columns: list[str],
        label_columns: list[str],
        model_factory,
        error_method: str = 'r2'
    ) -> dict:
    """Perform cross validation over a source dataset, using one device each time as the held out calibration/test dataset.

    The function also performs an internal k-fold cross validation within each device outer fold, as each fold_idx value in the
    dataset corresponds to a group of samples unseen in the other folds.
    
    Parameters
    ----------
    source_df: pd.DataFrame
        DataFrame containing the data to split into source, calibration, and test.
    wavenumber_columns: list[str]
        The list of wavenumber column names in the DataFrame. These are the features.
    label_columns: list[str]
        The list of label column names in the DataFrame
    model_factory: 
        Function to create a new untrained model object
    error_method: str, default = 'r2'
        Method to calculate error of predicted values versus true values in each fold. 
    
    Returns
    -------
    device_scores: dict
        The chosen error type calculated for each analyte for each outer device fold
    """

    devices = source_df['device'].unique().tolist()
    fold_indices = source_df['fold_idx'].unique().tolist()

    device_scores={}
    for device in devices:

        oof_predictions = []
        oof_true_values = []

        for fold_idx in fold_indices:

            # Create chosen model type
            model = model_factory()

            source_train, target_calibration, target_test  = generate_transfer_dataframes(source_df, device, fold_idx)
            
            model.fit(
                source_df=source_train,
                calibration_df=target_calibration,
                feature_columns=wavenumber_columns,
                label_columns=label_columns
            )

            predictions = model.predict(
                test_df=target_test,
                feature_columns=wavenumber_columns
            )

            oof_predictions.append(predictions)
            oof_true_values.append(target_test[label_columns].to_numpy())

        # Calculate chosen error for each analyte
        error_function = get_error_function(error_method)
        scores = error_function(
            true_values=np.concatenate(oof_true_values),
            predicted_values=np.concatenate(oof_predictions),
            how='by_analyte'
        )
        device_scores[device]={label: score for label,score in zip(label_columns, scores)}

    return device_scores