# Decisions

This document outlines the decisions and high level reasoning that have been made throughout the project.

# Preprocessing
1) Linear interpolation of wavenumber grids will be performed after data cleaning for all datasets. Looking at other research papers, this is often a good enough method due to Raman spectra being densely sampled anyway. If performance on the more sparsely sampled datasets is lower, perhaps this can be reevaluated.