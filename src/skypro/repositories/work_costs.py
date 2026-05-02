import json
from functools import cache

from skypro.config.settings import BASE_DIR


@cache
def load_work_costs() -> dict[str, int]:
    file_path = BASE_DIR / 'work_costs.json'
    try:
        with file_path.open() as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError('Failed to load work costs') from e
