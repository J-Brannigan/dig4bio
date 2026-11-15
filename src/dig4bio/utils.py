from dig4bio.paths import EXPERIMENTS_FOLDER
from pathlib import Path
import time
import nbformat

def create_experiment_from_template(experiment_name: str, experiment_number: int | None = None) -> None:
    """Create the next named experiment folder containing standardised files from the experiment template
    
    Trailing spaces will be removed from the provided experiment name and internal spaces will
    be replaced with an underscore.
    """

    folders = [
        'runs'
    ]
    
    files = [
        'notes.md',
        'plan.md'
    ]
    existing_experiment_count = sum(1 for item in EXPERIMENTS_FOLDER.iterdir() if item.is_dir()) + 1
    experiment_number = experiment_number if experiment_number is not None else existing_experiment_count

    # Clean the experiment name
    experiment_name = experiment_name.strip().replace(' ','_').lower()

    # Create the experiment folder
    experiment_folder_name = f'exp_{experiment_number:03d}_{experiment_name}'
    experiment_folder_path = EXPERIMENTS_FOLDER / experiment_folder_name
    experiment_folder_path.mkdir(exist_ok=True)

    # Create internal folders
    for folder in folders:
        folder_path = experiment_folder_path / folder
        folder_path.mkdir(exist_ok=True)

    # Create internal files
    for file in files:
        file_path = experiment_folder_path / file
        file_path.touch()


    notebook_path = experiment_folder_path / 'notebook.ipynb'
    notebook = nbformat.v4.new_notebook()
    notebook.cells.append(
        nbformat.v4.new_code_cell(
                        source = """%load_ext autoreload
%autoreload 2
from dig4bio.paths import EXPERIMENTS_FOLDER
from dig4bio.utils import create_new_experiment_run""")
    )
    notebook.cells.append(
        nbformat.v4.new_code_cell(
            source = """EXPERIMENT_FOLDER = EXPERIMENTS_FOLDER / "experiment_folder_name"
run_folder = create_new_experiment_run(EXPERIMENT_FOLDER)""")
    )
    nbformat.write(notebook, notebook_path)

def create_new_experiment_run(experiment_folder: Path) -> Path:
    """Create a new experiment run folder in the <current experiment>/runs/run<run number> folder ready for new submissions.
    
    This keeps new submission generations from overwriting eachother. If no experiment folder is given, the function
    will create the run subfolder in the runs folder within the experiment of the calling script."""

    runs_subfolder = experiment_folder / 'runs'
    run_count = len([p for p in runs_subfolder.iterdir() if p.is_dir()])
    current_timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')

    new_run_folder = runs_subfolder / f'run-{current_timestamp}'
    new_run_folder.mkdir(exist_ok=True)

    return new_run_folder