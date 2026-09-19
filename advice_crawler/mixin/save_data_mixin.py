from abc import ABC

class SaveDataMixin(ABC):

    def save_data(self, data: list[DataclassInterface]): # type: ignore
        ...