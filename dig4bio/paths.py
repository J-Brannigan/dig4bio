from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_DATA_FOLDER = DATA_FOLDER / "raw"

TRANSFER_PLATE_PATH = DATA_FOLDER / "raw" / "training" / "transfer_plate.csv"
TEST_SAMPLES_PATH = DATA_FOLDER / "raw" / "test" / "96_samples.csv"