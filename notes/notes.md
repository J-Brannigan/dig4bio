# 1. EDA

## 1.1 8 Devices
- There are a few hundred measurements from each device

## 1.2 Transfer Plate
- There are 2 measurements per sample

# 2. Plan

## 2.1 CV Strategy
Possibly a type of leave-one-device-out CV. Repeat this for each of the 8 devices:
- Label one device as the 'target'
- Split the target device data into train and test. Train is labelled, test is not (i.e remove the analyte concentration columns).
- Train on all other 7 devices completely.
- Calibrate on the target train dataset.
- Use this to predict the target test dataset analyte concentrations
- Calculate the prediction error. This is the error for this fold
- Repeat for the next fold
With this, the transfer plate and the 96 samples test dataset would not be used in the cross validation. They would only be used at prediction time

## 2.2 Prediction Methods
### 2.2.1 Baselines

These will give some insights into how well differently trained models generalise to unseen devices. Perhaps the simple baseline will perform roughly on par with the knowledge
transfer baseline which may suggest that we won't gain much from the knowledge transfer task.

1) **Simple Baseline**:
    - All data from 8 devices trained with a linear regression model
    - Predict the 96 samples test set using this model.
2) **Device Baseline**:
    - Transfer plate data trained with a linear regression model
    - Predict the 96 samples test set using this model
3) **Knowledge Transfer Baseline**:
    - All data from 8 devices trained with a linear regression model (model A)
    - Predict all transfer plate values and calculate error
    - Train another model (model B) to correct the predictions of model A
    - Predict the 96 samples dataset using model A

## 2.3 Calibration



# 3. Questions
- Is using a calibration step better than just training on the 8 devices and not using the transfer plate?
- How does the calibration pipeline perform compared to only using the transfer plate to train on
- Where does most of the variance come from? Is it chemical or instrumental?

# 4. Notes
As there are repeated measurements of the same sample in the transfer plate dataset, the same sample should not be in both train and test datasets.