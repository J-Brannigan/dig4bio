# Roadmap

## Contents

- [1. Clean Datasets ✅](#1-clean-datasets)
  - [1.1 Clean 8-device datasets ✅](#11-clean-8-device-datasets-)
  - [1.2 Clean transfer plate dataset ✅](#12-clean-transfer-plate-dataset-)
  - [1.3 Clean 96-sample dataset ✅](#13-clean-96-sample-dataset-)
- [2. Standardise Wavenumber Grids ✅](#2-standardise-wavenumber-grids)
- [3. Implement CV Strategy 🚧](#3-implement-cv-strategy)
- [4. Perform Baseline Experiments](#4-perform-baseline-experiments)

## Current Priority 🚧

[3. Implement CV Strategy ](#3-implement-cv-strategy).

## Project Gates
- Clean datasets ✅
- Choose shared wavenumber grid strategy ✅
- Transform all spectra to shared grid ✅
- Combine 8-device training data ✅
- Implement CV strategy
- Run baseline experiments
- Run calibration / transfer experiments

# 1. Clean Datasets
This is just basic cleanup - ensuring no nulls, standarising columns shapes, removal of erroenous characters
## 1.1 Clean 8-device datasets ✅

### Status:
Completed

### **Description:**
Standardise the eight source datasets so they share a consistent structure and can be processed together.

### **Tasks:**
- Check for missing or invalid values.
- Clean column names.
- Separate spectral measurements from concentration labels.
- Record each device's wavenumber grid.

### **Output:**
- One cleaned csv file per source device. ✅
- A reusable transformation function. ✅
- A reusable CLI command. ✅
- A short summary of each device's shape, target columns, sample count and wavenumber range. ✅

## 1.2 Clean transfer plate dataset ✅

### Status:
Complete

### **Description:**
Clean transfer plate dataset ready for shared-grid transformation.

Notes:
- Removed square brackets from spectral columns.
- Labelled spectral columns with wavenumbers.
- Stripped whitespace from sample names.
- Forward-filled sample names due to repeated measurements.

### **Output:**
- One cleaned csv file for the transfer plate. ✅
- A reusable transformation function. ✅
- A reusable CLI command. ✅
- A short summary of the data shape, target columns, sample count and wavenumber range. ✅

## 1.3 Clean 96-sample dataset ✅

### Status:
Complete

### **Description:**
Clean 96-sample dataset ready for shared-grid transformation.

Notes:
- Removed square brackets from spectral columns.
- Labelled spectral columns with wavenumbers.
- Stripped whitespace from sample names.
- Forward-filled sample names due to repeated measurements.

### **Output:**
- One cleaned csv file for the 96-sample plate. ✅
- A reusable transformation function. ✅
- A reusable CLI command. ✅
- A short summary of the data shape, target columns, sample count and wavenumber range. ✅

# 2. Standardise Wavenumber Grids ✅
### Status:
Complete

### **Description:**
Raman spectra from different devices may use different wavenumber grids. To train models across devices and predict consistently, all spectra need to be represented on a common grid.

### **Goal:**
Define and implement the shared wavenumber grid strategy

Options:
- Use a fixed manually chosen grid over the common wavenumber range.
- Use the intersection of all device grids.
- Define the grid from training data only inside each CV fold.
- Use one global grid based only on x-axis positions, not labels or intensities.

Notes:
- A single shared wavenumber strategy has been implemented - pick a start and end wavenumber and a wavenumber step size, and generate a grid. Then interpolate each spectra onto that grid.
- Most of the time a grid over the fingerprint region (300-1800)cm^-1 with single cm^-1 steps and linear b-spline interpolation will be used, but yaml config files can be used to change this approach easily.

### **Output:**
- Documented chosen grid strategy ✅
- A reusable transformation function. ✅
- All cleaned datasets transformed to the same spectral columns.✅

# 3. Implement CV Strategy 🚧
### Status:
Status: In Progress

### **Description:**
To ensure the performances we measure are accurate to the true performance, we need to implement a cross validation strategy. This will require us to train and test the model multiple times and then consider the spread and average.

### **Goal:**
- Define and implement a reusable cross validation strategy

Notes:
- Although we will likely just be using the main cross validation across the shared grid source dataset, we will also need to write a function for cross validation across one dataset ready for attempting to measure performance on just the transfer plate.

### **Output:**
- Documented cross validation strategy/strategies
- A resusable cross validation function/functions

# 4. Perform Baseline Experiments
### Status:
Status: Ready

### **Description:**
We should get an idea of how various simple models and apporaches work on the data we have before we try to implement more complex techniques. This gives us a baseline performance to beat.

### **Goal:**
Produce rough baseline performance goal(s) for more advanced models to beat

### **Options:**
We should try out
- Train on the transfer plate only, test on the 96 samples with k-fold CV. Use linear regression.
- Train on the shared grid source dataset, using one device in each fold as the 'transfer + test' set. Use linear regression.
- Calculate the average of each analyte from the shared grid source dataset and use those values as fixed predictions.