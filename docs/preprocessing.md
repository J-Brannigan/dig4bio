# Methods

1) **Spike removal**
    - Modified-Z-Score
2) **Baseline correction**
    - Sometimes this over corrects, as the flourescence background may not be the same shape in all situations
    - Sometimes just doing Savitzky-Golay is better
    Options:
        - Polynomial correction - Classic, simple
        - Rubberband correction
        - Asymmetric Least Squares, ALS - Most common automatic baseline
        - airPLS / arPLS / improved ALS variants - Improved versions of ALS
        - SNIP - Good for lots of peaks on a broad background74
3) **Smoothing**
    Options:
        - Savitzky-Golay (Can be a form of baseline correction)
        - Moving Average 
4) **Region Selection**
    - Fingerprint Region is usually 300-2000 cm-1
5) **Normalisation**
    This should be done AFTER flourescence background removal
    Options:
        - Area/total intensity normalisation
        - Standard Normal Variate, SNV
6) **Mean Centering**
7) **Direct Standardisation**
    - Choose a master instrument.
    - Train a DS earn a transformation from:
        - New instrument spectrum -> Master instrument spectrum
    - Apply that transformation to future spectra from the new instrument.
    - Feed the transformed spectra into the concentration model.