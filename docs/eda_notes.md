## 1 8 Devices
- There are a few hundred measurements from each device
- There are no nulls

## 2 Transfer Plate
There are 2 measurements per sample

# 3 Notes
As there are repeated measurements of the same sample in the transfer plate dataset, the same sample should not be in both train and test datasets.

# Folds
There seems to be a fold_idx value in each of the 8 device data. This seems to be some sort of predefined cross validation folding? We should probably try our own folding methods first, but fall back to this to see if there is a performance improvement gained by using it.

# Nulls
There are no nulls in any of the 8 device, transfer plate, 

# Intensities

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
| transfer_plate | 987 | 65535 | 4333.78 |

Intensities vary a lot between devices, and so these will need to be normalised in some way if we are to relate measurements.

# Wavenumbers

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

As the datasets do not use the same grid of wavenumbers, we will need to consider how to relate them together.
