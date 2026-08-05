The performance was the opposite of what I predicted it would be:

## Hypothesis
The performance of the methods (from highest to lowest will be)
1) Linear Sources
2) Linear Target
3) Averages Target
4) Averages Sources

## Actual Results
Although average r^2 isn't strictly correct, the average performance of the methods:
1) Averages Sources: -0.009
2) Averages Target: -0.013
3) Linear Target: -0.610
4) Linear Sources: -1225.549

## Findings
- Linear regression seems to be a very bad performer on both the target and sources datasets, not even performing better than average.
- Looking at the public leaderboard, only 122/172 teams beat an r^2 score of 0.0.

## Discussion

The core question - Why did the Linear models perform so badly?
- Perhaps this is because the number of features (1500) is much larger than the number of training examples (a few hundred at maximum, not even including breaking this down into folds) so it could be overfitting? An unregularised linear model therefore may just fit to noise, getting a perfect score on the training set whilst reducing out-of-sample robustness.
- I would also expect features that are close to one another to be highly correlated, so it would be useful to check the degree of multicollinearity. Multicollinearity can make the coefficients of a linear regression model unstable, meaning that small changes in the training data may lead to large changes in the estimated coefficients. This may reduce out-of-sample robustness.
- It does seem like the out-of-sample examples lie within the same distribution, as the averages have non-negative performance. However, this could be something to check.

## Conclusion
- A good baseline r^2 score to beat is 0.0.
- A non-regularised linear regressor is not the best model to use.

## Ideas
- Check how correlated the features are (could use VIF)
- Check if the performance of a linear model on the training sets are perfect. This would suggest overfitting.
- Check how similar each of the datasets are for the same samples. For example, is one device wildly different to the others?