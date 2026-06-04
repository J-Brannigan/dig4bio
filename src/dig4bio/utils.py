from pathlib import Path
from dig4bio.paths import RAW_DATA_FOLDER, INTERIM_DATA_FOLDER, PROCESSED_DATA_FOLDER

def get_level_path (level: str) -> Path:

    folder_map = {
        'raw': RAW_DATA_FOLDER,
        'interim': INTERIM_DATA_FOLDER,
        'processed': PROCESSED_DATA_FOLDER
    }

    return folder_map[level]