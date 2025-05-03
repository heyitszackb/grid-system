from typing import List
from .entity import Entity


class ResourceCollection(Entity):
    unused_names = [
        "Collection1",
        "Collection2",
        "Collection3",
        "Collection4",
        "Collection5",
        "Collection6",
        "Collection7",
        "Collection8",
        "Collection9",
        "Collection10",
        "Collection11",
        "Collection12",
        "Collection13",
    ]
    used_names: List[str] = []

    def __init__(self, name: str = ""):
        super().__init__(name)

    def process(self, entities: List[Entity]):
        for entity in entities:
            if isinstance(entity, ResourceCollection):
                self.resources.extend(entity.resources)
