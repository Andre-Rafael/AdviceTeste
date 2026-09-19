from abc import ABC
from typing import Any


class SaveDataMixin(ABC):

    def save(self, data: list[Any]): 
        ...