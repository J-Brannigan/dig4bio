import pandas as pd
from sklearn.exceptions import NotFittedError
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.utils.validation import check_is_fitted
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
        self.is_fitted_ = False

    def fit(self,X: np.ndarray, y: np.ndarray, X_calibration: np.ndarray, y_calibration: np.ndarray) -> Self:
        """Fit the prediction model to the source device data, and fit the calibration model to the prediction model residuals.
        
        Parameters
        ----------
        X: np.ndarray
            Numpy array containing the source device feature data to train on
        y: np.ndarray
            Numpy array containing the source device label data to train on
        X_calibration: np.ndarray
            Numpy array containing the calibration device feature data to calibrate on
        y: np.ndarray
            Numpy array containing the calibration device label data to calibrate on

        Returns
        -------
        self: CalibratedTransferRegressor
            Fitted regressor.
        """
        self.prediction_model.fit(X,y)

        calibration_predictions = self.prediction_model.predict(X_calibration)
        calibration_residuals = y_calibration - calibration_predictions

        self.calibration_model.fit(X_calibration, calibration_residuals)

        self.is_fitted_ = True

        return self
    
    def predict(self,x_test: np.ndarray) -> np.ndarray:
        """Using the combined fitted calibrated model pair, predict analyte concentrations.
        
        Parameters
        ----------
        x_test: np.ndarray
            Test data to predict

        Returns
        -------
        calibrated_predictions: np.ndarray
            Array of test data predictions with shape (n_samples, n_analytes)
        """
        check_is_fitted(self,'is_fitted_')

        initial_predictions = self.prediction_model.predict(x_test)
        predicted_residuals = self.calibration_model.predict(x_test)

        calibrated_predictions = initial_predictions + predicted_residuals

        return calibrated_predictions
    

class AveragePredictor(BaseEstimator, RegressorMixin):
    """Regressor that calculates the average for each analyte and always predicts those values.

    This regressor is meant to produce a scoring baseline.
    """
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Calculate the average of each analyte as the predictor"""

        self.mean_ = np.mean(y,axis=0)
        return self
    
    def predict(self, x: np.ndarray):
        """Return analyte averages as the predictions for each row"""
        check_is_fitted(self,'mean_')

        return np.tile(self.mean_, (len(x),1))


def train_model(model, train_df: pd.DataFrame, feature_columns:list[str], label_columns: list[str], calibration_df: pd.DataFrame = None, **fit_params):
    """Train a model on features (X) and labels (y) and calibrate on calibration data if given"""

    X_train = train_df[feature_columns].to_numpy()
    y_train = train_df[label_columns].to_numpy()

    if calibration_df is not None:
        X_calibration = calibration_df[feature_columns].to_numpy()
        y_calibration = calibration_df[label_columns].to_numpy()
        model.fit(X_train, y_train, X_calibration, y_calibration, **fit_params)
    else:
        model.fit(X_train, y_train, **fit_params)
    
    return model

def create_model_factory(prediction_model, calibration_model=None):
    """Create a reusable function to create a new regressor object with the chosen internal model types
    
    This is useful when a new model has to be created within each fold.
    """

    if calibration_model is None:
        def factory():
                return clone(prediction_model)
    else:
        def factory():
            return CalibratedTransferRegressor(
                prediction_model=clone(prediction_model),
                calibration_model=clone(calibration_model),
            )

    return factory
