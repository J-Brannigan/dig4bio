# Project Structure

This project is organised to keep data, exploration, reusable code, experiment definitions, experiment outputs, and result summaries separate.

```text
project/
    data/
        raw/
        interim/
        processed/

    notebooks/
    docs/

    scripts/

    src/
        dig4bio/

    configs/
        experiments/

    experiments/
        exp_001_name/
            plan.md
            notes.md
            runs/
                run_001/

    results/
```

## Folder Roles

`data/` contains datasets at different processing stages.

`data/raw/` is for original, untouched input data.

`data/interim/` is for cached, partially cleaned, or intermediate data.

`data/processed/` is for final modelling-ready data.

`notebooks/` is for exploration, visual checks, debugging, and error analysis. Reusable logic should move into `src/dig4bio/`.

`docs/` is for project-level notes, decisions, assumptions, and strategy.

`scripts/` is for CLI-oriented entry points and runnable project commands, such as experiment runners or data cleaning scripts.

`src/dig4bio/` is the reusable Python package used by notebooks, scripts, and experiments.

`configs/experiments/` contains editable experiment recipes.

`experiments/` contains experiment plans, notes, and recorded run outputs.

`results/` contains global summaries used to compare experiments and runs.

## Package Convention

Reusable Python code should live under `src/dig4bio/`.

Notebooks and scripts should import project code from the package:

```python
from dig4bio.utils import read_raman_file
```

Install the package in editable mode from the project root:

```bash
python -m pip install -e .
```

## Experiment Convention

An experiment is the question being tested.

A run is one recorded execution of that experiment.

```text
Experiment = the question
Run        = one execution of that question
```

Use numbered experiment folders:

```text
experiments/
    exp_001_baselines/
    exp_002_preprocessing/
    exp_003_model_families/
```

Each experiment folder should contain:

```text
plan.md     # Question, hypothesis, fixed variables, variables being tested
notes.md    # Results, issues, conclusions, and next steps
runs/       # Recorded executions
```

Each run folder should contain the frozen config and outputs from that execution:

```text
experiments/exp_001_baselines/runs/run_001/
    config.yaml
    metrics.csv
    fold_scores.csv
    predictions.csv
    plots/
    logs/
```

The config in `configs/experiments/` is the editable recipe. The config copied into a run folder is the frozen record of what actually ran.

## Naming Convention

Use names that describe the purpose of the experiment, not the expected outcome.

Good:

```text
exp_001_baselines
exp_002_preprocessing
exp_003_model_families
exp_004_calibration_transfer
```

Avoid:

```text
exp_002_best_model
exp_003_final_attempt
exp_004_random_tests
```

Use numbered run folders:

```text
run_001
run_002
run_003
```

## What Goes Where

```text
Raw downloaded data              -> data/raw/
Intermediate or cached data       -> data/interim/
Final modelling-ready data        -> data/processed/

Exploration                      -> notebooks/
CLI scripts and runnable commands -> scripts/
Reusable Python code              -> src/dig4bio/
Project-level notes               -> docs/

Editable experiment config         -> configs/experiments/exp_xxx.yaml
Experiment plan                    -> experiments/exp_xxx/plan.md
Experiment notes                   -> experiments/exp_xxx/notes.md
Run-specific outputs               -> experiments/exp_xxx/runs/run_xxx/

Global result comparisons          -> results/
```

## Principles

* Keep raw data untouched.
* Keep exploratory notebooks separate from reusable package code.
* Keep CLI scripts thin; reusable logic should live in `src/dig4bio/`.
* Keep project-level strategy separate from experiment-specific notes.
* Keep editable configs separate from frozen run configs.
* Save enough information for each run to understand and reproduce it later.
* Compare important runs using global summaries in `results/`.
