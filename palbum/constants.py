from enum import Enum


class PhotoOrder(str, Enum):
    RANDOM = "random"
    SEQUENTIAL = "sequential"

    @classmethod
    def get_form_choices(cls):
        return [
            (value.value, key.title()) for key, value in PhotoOrder.__members__.items()
        ]
