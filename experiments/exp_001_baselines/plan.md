## Question
What should the performance bar look like?

## Description

This Experiment aims to get a baseline for the performance of models trained on the datasets available. These should be a few very simple methods that
we will aim to beat with more complex models.

If a more complex model does not hit the bars set by this experiment, then it is needlessly complex and should be discarded.


## Hypothesis
The performance of the methods (from highest to lowest will be)
1) Linear Regression over the shared grid source dataset (Cross validated)
2) Transfer plate only Train + Test with k-fold CV over groups of samples. Use linear regression.
3) Analyte averages in the shared grid source dataset (Cross validated)