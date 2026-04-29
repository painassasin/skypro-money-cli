import json
from functools import cache
from typing import Literal

from config import BASE_DIR

type WorkType = Literal['ДЗ', 'КР', 'ДР', 'Лайв', 'ИК']
type WorkCost = int


@cache
def get_work_costs() -> dict[WorkType, WorkCost]:
    file_path = BASE_DIR / 'work_costs.json'
    return json.loads(file_path.read_text())
