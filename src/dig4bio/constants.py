import numpy as np

SOURCE_DEVICE_NAMES: tuple[str, ...] = (
    'anton532',
    'anton785',
    'kaiser',
    'metrohm',
    'mettler',
    'tec',
    'timegate',
    'tornado',
)

ALL_DEVICE_NAMES: tuple[str, ...] = SOURCE_DEVICE_NAMES + ('transfer_plate','96_samples')

DATASET_NAME_ALIASES: dict[str, str] = {
    'anton532': 'anton_532',
    'anton785': 'anton_785',
    'mettler': 'mettler_toledo',
    'tec': 'tec5',
    'transfer': 'transfer_plate',
    '96': '96_samples',
}

FINGERPRINT_GRID = np.arange(300,1801,1)