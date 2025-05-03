from typing import List

from components.grid import Grid
from .entity import Entity
from const import DIRECTION


class Conveyor(Entity):
    unused_names = [
        "Zippy",
        "Rolly",
        "Glide",
        "Slider",
        "Belt",
        "Carry",
        "Scoot",
        "Ferry",
        "Shuttle",
        "Flow",
        "Dash",
        "Hustle",
        "Whisk",
        "Drift",
        "Haul",
        "Cruise",
        "Tread",
        "Chug",
        "Surge",
        "Rush",
    ]
    used_names: List[str] = []

    def __init__(self, name: str = "", direction: DIRECTION = DIRECTION.RIGHT):
        super().__init__(name)
        self.direction: DIRECTION = direction

    def process(self, entities: List[Entity]):
        for entity in entities:
            pass

    def move(
        self, tmp_grid: Grid, row: int, col: int, entities: List["Entity"]
    ) -> tuple[int, int]:
        return row, col
