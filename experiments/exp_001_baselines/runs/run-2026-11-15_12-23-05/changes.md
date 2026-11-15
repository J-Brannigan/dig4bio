This fixes a bug. When grouping by sample, the rows were being sorted by sample, so were not in their original order which I was assuming.

Previously:

output_df = (
    test_df.copy()
    .groupby(by='sample')
    .mean()
    .reset_index()
)[LABEL_COLUMNS]

After:

output_df = (
    test_df.copy()
    .groupby(by='sample',sort=False)
    .mean()
    .reset_index()
)[LABEL_COLUMNS]