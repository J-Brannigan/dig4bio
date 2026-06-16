# Roadmap

## Contents

- [1. Clean Datasets ✅](#1-clean-datasets)
  - [1.1 Clean 8-device datasets ✅](#11-clean-8-device-datasets-)
  - [1.2 Clean transfer plate dataset ✅](#12-clean-transfer-plate-dataset-)
  - [1.3 Clean 96-sample dataset ✅](#13-clean-96-sample-dataset-)
- [2. Standardise Wavenumber Grids](#2-standardise-wavenumber-grids)

## Current Priority 🚧

## Project Gates
- Clean datasets ✅
- Choose shared wavenumber grid strategy
- Transform all spectra to shared grid
- Combine 8-device training data
- Implement CV strategy
- Run baseline experiments
- Run calibration / transfer experiments

# 1. Clean Datasets
This is just basic cleanup - ensuring no nulls, standarising columns shapes, removal of erroenous characters
## 1.1 Clean 8-device datasets ✅

### Status:
In Progress

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

# 2. Standardise Wavenumber Grids
### Status:
Not started

### **Description:**
Raman spectra from different devices may use different wavenumber grids. To train models across devices and predict consistently, all spectra need to be represented on a common grid.

### **Goal:**
Define and implement the shared wavenumber grid strategy

Options:
- Use a fixed manually chosen grid over the common wavenumber range.
- Use the intersection of all device grids.
- Define the grid from training data only inside each CV fold.
- Use one global grid based only on x-axis positions, not labels or intensities.

### **Output:**
- Documented chosen grid strategy
- A reusable transformation function.
- All cleaned datasets transformed to the same spectral columns.

# 3. Perform Baseline Experiments

Status: Blocked by shared-grid strategy

Goal:
Combine the cleaned 8-device datasets into one training dataframe.