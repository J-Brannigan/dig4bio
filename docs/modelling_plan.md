# 1 CV Strategy

Each row in each of the 8 spectra datasets contains a CV index number (from 0 to 4 inclusive).

From the [source paper](https://doi.org/10.1016/j.saa.2025.125861):
> As the number of samples per spectrometer is rather low for a machine learning problem, we use cross-validation to evaluate the performance of a specific model type on the data set of one spectrometer. Therefore, the samples are divided into five different folds so that the spectra of one sample all belong to the very same fold. To increase the comparability between the spectrometer data sets, the samples are part of the same fold across the different spectrometers, since the attribution of which spectrum belongs to which fold has quite some influence on the overall performance. Consequently, the attribution is part of the published data set, it can be found in the column “fold_idx” in the CSV files.

Therefore the CV strategy we will use is
```
for target_device in devices:
    for k in 0,1,2,3,4:
        target_test = target_device where fold_idx == k

        target_calib = target_device where fold_idx != k

        source_train = other devices where fold_idx != k

        train/adapt on source_train + target_calib
        predict target_test 
```

or in plain english:

- Repeat this for each of the 8 devices:
    - Repeat this for each fold index k:
        - Label one device as the 'target', and all 7 others as sources 1-7.
        - The 'Test' set will be all records in the target dataset where the fold index equals k
        - the 'Calibration' set will be all records in the target dataset where the fold index does not equal k
        - The 'Training' set will be all records in the sources dataset where the fold index does not equal k
        - Train on the training set
        - Calibrate on the calibration set
        - Use this model to to predict the test set analyte concentrations
    - Combine all fold predictions
    - Calculate the prediction error of the combined fold predictions. This is the error for this device.

With this method, the transfer plate and the 96 samples test dataset would not be used in the cross validation. They would only be used at prediction time

# 2 Prediction Methods
## 2.1 Baselines

These will give some insights into how well differently trained models generalise to unseen devices. Perhaps the simple baseline will perform roughly on par with the knowledge transfer baseline which may suggest that we won't gain much from the knowledge transfer task.

1) **Simple Baseline**:
    - All data from 8 devices trained with a linear regression model
    - Predict the 96 samples test set using this model.
2) **Device Baseline**:
    - Transfer plate data trained with a linear regression model
    - Predict the 96 samples test set using this model
3) **Knowledge Transfer Baseline**:
    - All data from 8 devices trained with a linear regression model (model A)
    - Predict all transfer plate values and calculate error
    - Train a linear regression model (model B) to correct the predictions of model A
    - Predict the 96 samples dataset using model A

## 2.2 Residual Correction

1) **Residual Prediction (CV)**
    - Use the CV strategy above
    - Calibration method = train a model to predict how far off each predicted analyte is and then apply the change
    - The calibration should be trained on only 96 of the target device's labelled rows, and then the remaining of the target device's rows should be used to measure the performance.

# 4. Questions
- Is using a calibration step better than just training on the 8 devices and not using the transfer plate?
- How does the calibration pipeline perform compared to only using the transfer plate to train on
- Where does most of the variance come from? Is it chemical or instrumental?