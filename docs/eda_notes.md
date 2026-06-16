# EDA Notes

## Contents

- [1. 8 Devices](#1-8-devices)
  - [1.1 MSM_present](#11-msm_present)
- [2. Transfer Plate](#2-transfer-plate)
- [3. Counts](#3-counts)
- [4. Folds](#4-folds)
- [5. Nulls](#5-nulls)
- [6. Intensities](#6-intensities)
- [7. Wavenumbers](#7-wavenumbers)

## 1. 8 Devices
- There are a few hundred measurements from each device
- There are no nulls
### 1.1 MSM_present
There is a 'MSM_present' column which is not in the transfer plate or 96 sample test dataset. This column means whether mineral salt medium was present in that sample. It was added to some samples to mimic realistic bacterial fermentation/supernatant conditions.

As it's not in the test dataset, we should probably just treat this as a nuisance column and remove it before modelling or learned preprocessing.

## 2. Transfer Plate
There are 2 measurements per sample

There are repeated measurements of the same sample in the transfer plate dataset, the same sample should not be in both train and test datasets.

## 3. Counts

| Dataset | Row Count | Column Count |
| ------- | ------------: | ------------: |
| anton532 | 270 | 1656 |
| anton785 | 270 | 1106 |
| kaiser | 134 | 6598 |
| metrohm | 399 | 1922 |
| mettler | 275 | 2906 |
| tec | 395 | 3131 |
| timegate | 133 | 516 |
| tornado | 385 | 3006 |
| | | |
| Transfer Plate | 192 | 2052 |
| | | |
| 96 Samples | 192 | 2049 |

## 4. Folds
There seems to be a fold_idx value in each of the 8 device data. This is predefined folds as in the [source paper](https://doi.org/10.1016/j.saa.2025.125861), where each fold contains the same samples across all devices (e.g sample A is in fold 2 for each of the 8 devices).

| Dataset | Fold 0 Count | Fold 1 Count | Fold 2 Count | Fold 3 Count | Fold 4 Count |
| ------- | -----: | -----: | -----: | -----: | -----: |
| anton532 | 50 | 55 | 55 | 55 | 55 |
| anton785 | 50 | 55 | 55 | 55 | 55 |
| kaiser | 26 | 27 | 27 | 27 | 27 |
| metrohm | 80 | 80 | 80 | 80 | 79 |
| mettler | 55 | 55 | 55 | 55 | 55 |
| tec | 75 | 80 | 80 | 80 | 80 |
| timegate | 26 | 27 | 26 | 27 | 27 |
| tornado | 75 | 75 | 80 | 75 | 80 |

## 5. Nulls
| Dataset | Number Of Null Values |
| ------- | ------------: | 
| 8 Devices | 0 |
| Transfer Plate | 0 |
| 96 Samples | 0 |

## 6. Intensities

| Dataset | Min Intensity | Max Intensity | Mean Intensity |
| ------- | ------------: | ------------: | -------------: |
| anton532 | 1009.39 | 12267.88 | 2197.2 |
| anton785 | 443.91 | 6985.63 | 844.66 |
| kaiser | 2.6 | 11191.95 | 2400.28 |
| metrohm | 1057 | 25064 | 2173.05 |
| mettler | 99.11 | 54678.71 | 5268.84 |
| tec | 0 | 43539.53 | 5092.86 |
| timegate | 0.000043	 | 0.0051 | 0.00057 |
| tornado | 251.38 | 91506.35 | 10174.18 |
| | | | |
| Transfer Plate | 987 | 65535 | 4333.78 |
| | | | |
| 96 Samples | 3012 | 6608 | 4917.14 |

Intensities vary a lot between devices, and so these will need to be normalised in some way if we are to relate measurements.

## 7. Wavenumbers

| Dataset  | Min Wavemumber | Max Wavenumber | Median Spacing | Roughly Evenly Spaced |
| ------- | ------ | ------- | ---: | ---:|
| anton532| 200 | 3500 | 2    | True  |
| anton785| 100 | 2300 | 2    | True  |
| kaiser  | -36.3 | 1941.3 | 0.3  | True  |
| metrohm | 202.22 | 3349.39 | 1.6  | False |
| mettler | 300 | 3200 | 1    | True  |
| tec     | 85  | 3210 | 1    | True  |
| timegate| 200.93 | 1997.69 | 3.48 | False |
| tornado | 300 | 3300 | 1    | True  |
|  |  |  |  |  |
| transfer_plate | 65 | 3350.00 | 1 | True |
| | | | |
| 96_samples |  65 | 3350.00 | 1 | True |

As the datasets do not use the same grid of wavenumbers, we will need to consider how to relate them together.
