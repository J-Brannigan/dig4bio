from dig4bio.paths import EXPERIMENTS_FOLDER

def create_experiment_from_template(experiment_name: str, experiment_number: int | None = None):
    """Create the next named experiment folder containing standardised files from the experiment template
    
    Trailing spaces will be removed from the provided experiment name and internal spaces will
    be replaced with an underscore.
    """

    folders = [
        'runs'
    ]
    
    files = [
        'notebook.ipynb',
        'notes.md'
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