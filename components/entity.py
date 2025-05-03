from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
import random
from enum import Enum

if TYPE_CHECKING:
    from .grid import Grid


class Resource(Enum):
    WOOD = "Wood"
    METAL = "Metal"
    STONE = "Stone"


class Entity(ABC):
    unused_names: List[str] = []
    used_names: List[str] = []
    _id_counter: int = 0

    def __init__(self, name: str = ""):
        self.name: str = name if name else self.get_unique_name()
        self.id: int = Entity.get_unique_id()
        self.resources: List[Resource] = []

    @classmethod
    def get_unique_name(cls) -> str:
        if cls.unused_names:
            name = random.choice(cls.unused_names)
            cls.unused_names.remove(name)
            cls.used_names.append(name)
            return name
        return "Unnamed"

    @classmethod
    def get_unique_id(cls) -> int:
        Entity._id_counter += 1
        return Entity._id_counter

    def count_resource(self, resource_type: Resource) -> int:
        return sum(1 for resource in self.resources if resource == resource_type)

    @abstractmethod
    def process(self, entities: List["Entity"]) -> None:
        pass

    @abstractmethod
    def move(
        self, tmp_grid: "Grid", row: int, col: int, entities: List["Entity"]
    ) -> tuple[int, int]:
        pass
