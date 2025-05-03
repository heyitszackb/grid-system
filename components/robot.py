from typing import List, Optional

from components.conveyor import Conveyor
from components.grid import Grid
from .entity import Entity, Resource
from const import DIRECTION


class Robot(Entity):
    unused_names = [
        "bit",
        "zip",
        "cog",
        "tin",
        "dot",
        "buzz",
        "chip",
        "gear",
        "lex",
        "rok",
        "pip",
        "zed",
        "bop",
        "vim",
    ]
    used_names: List[str] = []

    def __init__(self, name: str = "", path: List[DIRECTION] = [DIRECTION.WAIT]):
        super().__init__(name)
        self.path = path
        self.current_move_index = 0

    def get_next_move(self) -> DIRECTION:
        if not self.path:
            raise ValueError("Path is empty. No moves available.")
        move = self.path[self.current_move_index]
        return move

    def get_previous_move(self) -> DIRECTION:
        if not self.path:
            raise ValueError("Path is empty. No moves available.")
        previous_index = (self.current_move_index - 1) % len(self.path)
        return self.path[previous_index]

    def update_move_index(self) -> None:
        if not self.path:
            raise ValueError("Path is empty. No moves available.")
        self.current_move_index = (self.current_move_index + 1) % len(self.path)

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    def set_path(self, path: List[DIRECTION]):
        self.current_move_index = 0
        self.path = path
        return True

    def process(self, entities: List[Entity]):
        for entity in entities:
            pass

    def _calc_new_position(
        self, row: int, col: int, direction: DIRECTION
    ) -> tuple[int, int]:
        new_row = row
        new_col = col
        if direction == DIRECTION.UP:
            new_row -= 1
        elif direction == DIRECTION.DOWN:
            new_row += 1
        elif direction == DIRECTION.LEFT:
            new_col -= 1
        elif direction == DIRECTION.RIGHT:
            new_col += 1
        elif direction == DIRECTION.WAIT:
            new_row += 0
            new_col += 0
        else:
            raise ValueError(f"Unknown direction: {direction}")
        return new_row, new_col

    def move(
        self, tmp_grid: Grid, row: int, col: int, entities: List["Entity"]
    ) -> tuple[int, int]:
        is_on_conveyor = False
        conveyor_direction = DIRECTION.WAIT
        for entity in entities:
            if isinstance(entity, Conveyor):
                is_on_conveyor = True
                conveyor_direction = entity.direction

        new_row = None
        new_col = None

        if is_on_conveyor:
            new_row, new_col = self._calc_new_position(row, col, conveyor_direction)
        else:
            new_row, new_col = self._calc_new_position(row, col, self.get_next_move())
            self.update_move_index()

        # if there is a robot in the cell we are trying to move to, we need to go back.
        is_robot_in_space = False
        for entity in tmp_grid.get_entities_at(new_row, new_col):
            is_robot_in_space = True

        if is_robot_in_space:
            return row, col
        return new_row, new_col
