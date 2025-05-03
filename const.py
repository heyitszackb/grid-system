from enum import Enum

from typing import TypeVar

from components.entity import Entity

T = TypeVar("T", bound=Entity)


class Command:
    def __init__(self, input_str: str) -> None:
        self.buffer = input_str
        self.parse()

    def parse(self) -> None:
        parts = self.buffer.split(maxsplit=1)
        if parts:
            self.value = parts[0]
            if len(parts) > 1:
                self.args = parts[1].split()
            else:
                self.args = []


class DIRECTION(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    WAIT = 5
