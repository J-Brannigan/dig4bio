# Dig4Bio

Kaggle project workspace for the Dig4Bio Raman transfer learning challenge.

## Structure

```text
data/                  # Raw, interim, and processed datasets
notebooks/             # Exploration, visual checks, debugging, and error analysis
docs/                  # Project notes, decisions, assumptions, and conventions
scripts/               # CLI-oriented scripts and runnable project commands
src/dig4bio/           # Reusable Python package code
configs/experiments/   # Editable experiment configs
experiments/           # Experiment plans, notes, and run outputs
results/               # Global result summaries
```

See `docs/project_structure.md` for the folder conventions and experiment/run structure.

## Package Setup

Install the project package in editable mode from the project root:

```bash
python -m pip install -e .
```

Then notebooks, scripts, and experiment code can import reusable functionality from `dig4bio`:

```python
from dig4bio.utils import read_raman_file
```
