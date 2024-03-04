import json
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum

IMAGES = [
    "paso_01.JPG",
    "paso_02.JPG",
    "paso_03.JPG",
    "paso_04.JPG",
    "paso_05.JPG",
    "paso_06.JPG",
    "paso_07.JPG",
]


class PhotoOrder(str, Enum):
    RANDOM = "random"

    @classmethod
    def get_form_choices(cls):
        return [
            (value.value, key.title()) for key, value in PhotoOrder.__members__.items()
        ]


@dataclass
class DisplaySettings:
    json_name = "display_settings.json"

    photo_order: str
    display_time: int
    fade: bool

    def to_dict(self):
        return asdict(self)

    def save(self):
        with open(self.json_name, "w") as outfile:
            json.dump(self.to_dict(), outfile)

    @classmethod
    def read(cls):
        with open(cls.json_name, "r") as read_file:
            data = json.load(read_file)
            return cls(**data)
