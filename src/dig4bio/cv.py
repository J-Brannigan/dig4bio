import pandas as pd
from dig4bio.datasets import get_fold_df
from dig4bio.evaluation import get_error_function
import numpy as np
from dig4bio.models import train_model

def cross_validate_sample_folds(
        df: pd.DataFrame,
        wavenumber_columns: list[str],
        label_columns: list[str],
        model_factory,
        error_method: str = 'r2',
        calibrate: bool = True
    ) -> dict:
    """Perform cross validation over a DataFrame, using one device within the DataFrame each time as the held out test dataset
    and (optionally) the calibration dataset.

    The function also performs an internal k-fold cross validation within each device outer fold, as each fold_idx value in the
    dataset corresponds to a group of samples unseen in the other folds.

    If calibrate = True, the model_factory must produce a CalibratedTransferRegressor object.
    
    Parameters
    ----------
    df: pd.DataFrame
        DataFrame containing the data to split into source, calibration, and test.
    wavenumber_columns: list[str]
        The list of wavenumber column names in the DataFrame. These are the features.
    label_columns: list[str]
        The list of label column names in the DataFrame
    model_factory: 
        Function to create a new untrained model object
    error_method: str, default = 'r2'
        Method to calculate error of predicted values versus true values in each fold.
    calibrate: bool, default = True
        Whether calibration data should be extracted from df and used to calibrate the model predictions
    
    Returns
    -------
    device_scores: dict
        The chosen error type calculated for each analyte for each outer device fold
    """

    devices = df['device'].unique().tolist()
    fold_indices = df['fold_idx'].unique().tolist()

    device_scores={}
    for device in devices:

        oof_predictions = []
        oof_true_values = []

        for fold_idx in fold_indices:

            source_df = get_fold_df(df, device, fold_idx, 'train')
            test_df = get_fold_df(df, device, fold_idx, 'test')

            if calibrate:
                calibration_df = get_fold_df(df, device, fold_idx, 'calibration')
            else:
                calibration_df = None
            
            predictions = execute_fold(model_factory, source_df, test_df, wavenumber_columns, label_columns, calibration_df)

            oof_predictions.append(predictions)
            oof_true_values.append(test_df[label_columns].to_numpy())

        # Calculate chosen error for each analyte
        error_function = get_error_function(error_method)
        scores = error_function(
            true_values=np.concatenate(oof_true_values),
            predicted_values=np.concatenate(oof_predictions),
            how='by_analyte'
        )
        device_scores[device]={label: score for label,score in zip(label_columns, scores)}

    return device_scores

def execute_fold(
        model_factory, 
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        feature_columns: list[str],
        label_columns: list[str],
        calibration_df: pd.DataFrame | None = None
    ) -> np.ndarray:
    """Create a model object, train the model on the training set, and use the model to predict a test set."""
    # Create chosen model type
    model = model_factory()
    
    model = train_model(
        model = model,
        train_df = train_df,
        feature_columns=feature_columns,
        label_columns=label_columns,
        calibration_df=calibration_df
    )

    predictions = model.predict(
        test_df[feature_columns].to_numpy()
    )

    return predictions