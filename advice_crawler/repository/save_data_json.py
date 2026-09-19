import json
from dataclasses import asdict
from typing import Any

from mixin.save_data_mixin import SaveDataMixin


class SaveDataJson(SaveDataMixin):

    def save(self, data: list[Any]):
        json_data = json.dumps([asdict(process) for process in data], sort_keys=True, default=str, indent=4)
        with open('data_collected.json', 'a', encoding='UTF-8') as f:
            f.write(json_data)