from typing import List, Optional

from components.grid import Grid
from .entity import Entity, Resource
from .robot import Robot


class Factory(Entity):
    unused_names = [
        "Spark",
        "Bolt",
        "Whirr",
        "Clank",
        "Weld",
        "Flux",
        "Crank",
        "Fuse",
        "Loop",
        "Jolt",
        "Meld",
        "Glim",
        "Zap",
        "Tick",
        "Puff",
    ]
    used_names: List[str] = []

    def __init__(self, name: str = "", resource_type: Resource = Resource.WOOD):
        super().__init__(name)
        self.resource_type = resource_type

    def deposit_to(self, robots: List[Robot] = []):
        for robot in robots:
            robot.add_resource(self.resource_type)

    def process(self, entities: List[Entity]):
        for entity in entities:
            if isinstance(entity, Robot):
                entity.add_resource(self.resource_type)

    def move(
        self, tmp_grid: Grid, row: int, col: int, entities: List["Entity"]
    ) -> tuple[int, int]:
        return row, col
