# Models

The below model families are the most often tried-and-tested for raman spectra.

1. Partial Least Squares Regression, PLSR
    - Usually the first serious baseline.
2. Regularised linear models: Ridge, Lasso, Elastic Net
    - Very good baseline family, especially when you want simplicity.
3. Support Vector Regression, SVR
    - Often one of the strongest nonlinear classical ML options.
4. Gaussian Process Regression, GPR
    - Strong nonlinear model, especially for small datasets, but can be expensive.
5. Neural networks: MLPs and 1D CNNs
    - Potentially powerful, but only worth it when the data supports it.
6. Multivariate Curve Resolution / component-based models
    - Useful when the task is mixture/component quantification.