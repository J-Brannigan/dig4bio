import numpy as np
from sklearn.metrics import r2_score

def calculate_r2(true_values: np.ndarray, predicted_values: np.ndarray, how: str = 'by_analyte') -> np.ndarray:
    """Calculate the coefficient of determination between a set of true and predicted values
    
    'how' determines whether r2 should be calculated separately for each prediction column or just one total value
    """
    if how == 'total':
        output_method = 'uniform_average'
    elif how == 'by_analyte':
        output_method = 'raw_values'
    else:
        raise ValueError(f'{how} is not a valid error_level for r^2 calculation.')
    
    scores = r2_score(true_values, predicted_values,multioutput=output_method)

    # r2_score can return a float so standardise to np.ndarray
    return np.array(scores)

def get_error_function(error_method: str):
    """Helper function to retrieve an error function by name"""
    if error_method == 'r2':
        return calculate_r2
    else:
        raise ValueError(f'{error_method} is not a currently supported error method')