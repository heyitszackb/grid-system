from typing import List, Iterator, Dict, Optional, Type, Union, TYPE_CHECKING
from .entity import Entity
from const import DIRECTION, T

if TYPE_CHECKING:
    from .entity import Entity


class Coord:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"Coord(row={self.row}, col={self.col})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coord):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))


class Grid:
    def __init__(self):
        self._entities_at_coord: Dict[Coord, List["Entity"]] = {}
        self._coord_of_entity: Dict["Entity", Coord] = {}

    def __iter__(self) -> Iterator[tuple[int, int, List["Entity"]]]:
        for coord, entities in self._entities_at_coord.items():
            yield (coord.row, coord.col, entities)

    def get_items(self) -> Iterator[tuple[int, int, List["Entity"]]]:
        for coord, entities in self._entities_at_coord.items():
            yield (coord.row, coord.col, entities)

    def get_entities_at(self, row: int, col: int) -> List["Entity"]:
        coord = Coord(row, col)
        return self._entities_at_coord.get(coord, [])

    def add_entity_at(self, row: int, col: int, entity: "Entity") -> bool:
        self.validate_entity(row, col, entity)
        if entity in self._coord_of_entity:
            raise ValueError(f"Entity {entity} already exists in the grid.")

        coord = Coord(row, col)
        self._entities_at_coord.setdefault(coord, []).append(entity)
        self._coord_of_entity[entity] = coord
        return True

    def remove_entity(self, entity: "Entity") -> bool:
        if entity not in self._coord_of_entity:
            return False

        coord = self._coord_of_entity[entity]
        self._entities_at_coord[coord].remove(entity)
        del self._coord_of_entity[entity]

        if not self._entities_at_coord[coord]:
            del self._entities_at_coord[coord]

        return True

    def get_entities(
        self, entity_type: Optional[Type[T]] = None
    ) -> Union[List[T], List["Entity"]]:
        all_entities = [
            entity
            for entities in self._entities_at_coord.values()
            for entity in entities
        ]
        if entity_type is None:
            return all_entities
        return sorted(
            (entity for entity in all_entities if isinstance(entity, entity_type)),
            key=lambda entity: entity.id,
        )

    def get_coord_of_entity(self, entity: "Entity") -> Optional[tuple[int, int]]:
        coord = self._coord_of_entity.get(entity, None)
        if coord is not None:
            return (coord.row, coord.col)
        return None

    def get_entity_by_id(self, entity_id) -> Optional["Entity"]:
        for entity in self._coord_of_entity.keys():
            if entity.id == entity_id:
                return entity
        return None

    def clear_entities(self) -> None:
        self._entities_at_coord = {}
        self._coord_of_entity = {}

    def copy_entities_from(self, other: "Grid") -> None:
        self.clear_entities()
        for row, col, entities in other:
            for entity in entities:
                self.add_entity_at(row, col, entity)

    def move_entity(self, to_row: int, to_col: int, entity: "Entity") -> bool:
        if self.remove_entity(entity):
            return self.add_entity_at(to_row, to_col, entity)
        return False

    def move_entity_in_direction(self, entity: "Entity", direction: DIRECTION) -> bool:
        if entity not in self._coord_of_entity:
            return False

        current_coord = self._coord_of_entity[entity]
        new_row, new_col = current_coord.row, current_coord.col

        if direction == DIRECTION.UP:
            new_row -= 1
        elif direction == DIRECTION.DOWN:
            new_row += 1
        elif direction == DIRECTION.LEFT:
            new_col -= 1
        elif direction == DIRECTION.RIGHT:
            new_col += 1
        else:
            raise ValueError(f"Unknown direction: {direction}")

        # Attempt to move the entity to the new position
        return self.move_entity(new_row, new_col, entity)

    def validate_entity(self, row: int, col: int, entity: "Entity") -> bool:
        # Check if the entity already exists in the grid
        if entity in self._coord_of_entity:
            raise ValueError(f"Entity {entity} already exists in the grid.")

        coord = Coord(row, col)
        entities_at_coord = self._entities_at_coord.get(coord, [])

        entity_type = type(entity)
        if any(isinstance(e, entity_type) for e in entities_at_coord):
            raise ValueError(f"You can only have one {entity_type.__name__} per cell")

        return True
