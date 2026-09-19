class InvalidException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class DataNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)