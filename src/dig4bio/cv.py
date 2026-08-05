import pandas as pd
from dig4bio.datasets import get_device_fold_df, get_fold_df
from dig4bio.evaluation import get_error_function
import numpy as np
from dig4bio.models import train_model

def augmented_cross_validate_sample_folds(
        df: pd.DataFrame,
        wavenumber_columns: list[str],
        label_columns: list[str],
        model_factory,
        test_df: pd.DataFrame | None = None,
        error_method: str = 'r2',
        calibrate: bool = True,
        train_on_target: bool | None = False
    ) -> dict:
    """Perform cross validation over a DataFrame, using one device within the DataFrame each time as the held out test dataset
    and (optionally) the calibration dataset.

    The function also performs an internal k-fold cross validation within each device outer fold, as each fold_idx value in the
    dataset corresponds to a group of samples unseen in the other folds.

    If calibrate = True, the model_factory must produce a CalibratedTransferRegressor object.
    
    Parameters
    ----------
    df: pd.DataFrame
        DataFrame containing the data to split into source, calibration, and (optionally) test.
    wavenumber_columns: list[str]
        The list of wavenumber column names in the DataFrame. These are the features.
    label_columns: list[str]
        The list of label column names in the DataFrame
    model_factory: 
        Function to create a new untrained model object
    test_df: pd.DataFrame | None, default = None
        DataFrame containing the data to test on. Optional. If not given test data comes from df.
    error_method: str, default = 'r2'
        Method to calculate error of predicted values versus true values in each fold.
    calibrate: bool, default = True
        Whether calibration data should be extracted from df and used to calibrate the model predictions
    train_on_target: bool | None, default = None
        Whether the target device should be used as the train as well as the test dataset. Fold_idx will still ensure no leakage.
    
    Returns
    -------
    device_scores: dict
        The chosen error type calculated for each analyte for each outer device fold
    """

    error_function = get_error_function(error_method)

    devices = df['device'].unique().tolist()
    fold_indices = df['fold_idx'].unique().tolist()

    total_oof_predictions = []
    total_oof_true_values = []

    overall_scores={'total': {}, 'devices': {}}
    for device in devices:

        device_oof_predictions = []
        device_oof_true_values = []

        for fold_idx in fold_indices:

            source_df = get_device_fold_df(df, device, fold_idx, 'train', train_on_target)
            if test_df is None:
                fold_test_df = get_device_fold_df(df, device, fold_idx, 'test')
            else:
                fold_test_df = test_df[test_df['fold_idx']==fold_idx]

            if calibrate:
                calibration_df = get_device_fold_df(df, device, fold_idx, 'calibration')
            else:
                calibration_df = None
            
            predictions = execute_fold(model_factory, source_df, fold_test_df, wavenumber_columns, label_columns, calibration_df)

            device_oof_predictions.append(predictions)
            device_oof_true_values.append(fold_test_df[label_columns].to_numpy())
            total_oof_predictions.append(predictions)
            total_oof_true_values.append(fold_test_df[label_columns].to_numpy())

        # Calculate this chosen error of this device for each analyte
        device_scores = error_function(
            true_values=np.concatenate(device_oof_true_values),
            predicted_values=np.concatenate(device_oof_predictions),
            how='by_analyte'
        )
        overall_scores['devices'][device]={label: score for label,score in zip(label_columns, device_scores)}

    # Calculate the total chosen error for each analyte
    total_scores = error_function(
            true_values=np.concatenate(total_oof_true_values),
            predicted_values=np.concatenate(total_oof_predictions),
            how='by_analyte'
        )
    overall_scores['total']={label: score for label,score in zip(label_columns, total_scores)}

    return overall_scores

def cross_validate_sample_folds(
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        wavenumber_columns: list[str],
        label_columns: list[str],
        model_factory,
        error_method: str = 'r2',
    ) -> dict:
    """Perform k-fold cross validation over train and test DataFrames, ensuring within each fold that the same fold_idx value
    is not trained and tested on.

    Each fold_idx value in the dataset corresponds to a group of samples unseen in the other folds.
    
    Parameters
    ----------
    train_df: pd.DataFrame
        DataFrame containing the data to train on.
    test_df: pd.DataFrame
        DataFrame containing the data to test on.
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
    fold_scores: dict
        The chosen error type calculated for each analyte for each fold
    """
    fold_indices = train_df['fold_idx'].unique().tolist()

    fold_scores={}
    for fold_idx in fold_indices:

        fold_train_df = get_fold_df(train_df, fold_idx, 'train')
        fold_test_df = get_fold_df(test_df, fold_idx, 'test')
        
        predictions = execute_fold(model_factory, fold_train_df, fold_test_df, wavenumber_columns, label_columns)

        # Calculate chosen error for each analyte
        error_function = get_error_function(error_method)
        scores = error_function(
            true_values=fold_test_df[label_columns].to_numpy(),
            predicted_values=predictions,
            how='by_analyte'
        )

        fold_scores[fold_idx]={label: score for label,score in zip(label_columns, scores)}

    return fold_scores

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