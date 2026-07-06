import pandas as pd
from sklearn.exceptions import NotFittedError
import numpy as np
from sklearn.base import clone
from typing import Self

class CalibratedTransferRegressor:
    """Regressor that learns from source devices and calibrates predictions for a target device.
   
    The model first trains a prediction model on source device data, then applies
    a calibration model to adjust the predictions of the prediction model using 
    target device calibration samples.

    Parameters
    ----------
    prediction_model: estimator-like object
        The estimator-like object that will be trained on the source devices and produce initial predictions
    calibration_model: estimator-like object
        The estimator-like object that will be used to adjust the initial predictions.
        
    Attributes
    ----------
    prediction_model:
        Fitted or unfitted base prediction model.
    calibration_model:
        Fitted or unfitted calibration model.
    istrained:
        Whether the regressor has been fitted.
    """
    def __init__(self, prediction_model, calibration_model):
        self.prediction_model = prediction_model
        self.calibration_model = calibration_model
        self.istrained = False

    def fit(self,source_df: pd.DataFrame, calibration_df: pd.DataFrame, feature_columns: list[str], label_columns: list[str]) -> Self:
        """Fit the prediction model to the source device data, and fit the calibration model to the prediction model residuals.
        
        Parameters
        ----------
        source_df: pd.DataFrame
            DataFrame containing the source device data to initially train on
        calibration_df: pd.DataFrame
            DataFrame containing the target device data to calibrate on
        feature_columns: list[str]
            The list of feature column names in both DataFrames
        label_columns: list[str]
            The list of label column names in both DataFrames

        Returns
        -------
        self: CalibratedTransferRegressor
            Fitted regressor.
        """

        x_source = source_df[feature_columns]
        y_source = source_df[label_columns]

        x_calibration = calibration_df[feature_columns]
        y_calibration = calibration_df[label_columns]

        self.prediction_model.fit(x_source,y_source)

        calibration_predictions = self.prediction_model.predict(x_calibration)
        calibration_residuals = y_calibration - calibration_predictions

        self.calibration_model.fit(x_calibration, calibration_residuals)

        self.istrained = True

        return self
    
    def predict(self,test_df: pd.DataFrame, feature_columns: list[str]) -> np.ndarray:
        """Using the combined fitted calibrated model pair, predict analyte concentrations.
        
        Parameters
        ----------
        test_df: pd.DataFrame
            DataFrame containing the test data to predict
        feature_columns: list[str]
            The list of feature column names in the test DataFrame

        Returns
        -------
        calibrated_predictions: np.ndarray
            Array of test data predictions with shape (n_samples, n_analytes)
        """
        if not self.istrained:
            raise NotFittedError('Regressor must be trained before predictions are made')

        x_test = test_df[feature_columns]

        initial_predictions = self.prediction_model.predict(x_test)
        predicted_residuals = self.calibration_model.predict(x_test)

        calibrated_predictions = initial_predictions + predicted_residuals

        return calibrated_predictions
    

def train_model(model, X, y, **fit_params):
    """Train a model on features (X) and labels (y)"""
    model.fit(X, y, **fit_params)
    return model

def calibrated_transfer_model_factory(prediction_model, calibration_model):
    """Create a reusable function to create a new calibrated transfer regressor object with the chosen internal model types
    
    This is useful when a new model has to be created within each fold.
    """
    def factory():
        return CalibratedTransferRegressor(
            prediction_model=clone(prediction_model),
            calibration_model=clone(calibration_model),
        )

    return factory
