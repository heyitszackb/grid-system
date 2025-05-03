from typing import List, Optional

from components.grid import Grid
from .robot import Robot
from .entity import Entity
from const import DIRECTION


class GridManager:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def settle_entity_positions(self, grid: Grid) -> List[Entity]:
        new_settled_entities: List[Entity] = []
        for _, _, entities in grid:
            # only one will have a wait action, can't be in the same space any other way.
            robots = [entity for entity in entities if isinstance(entity, Robot)]
            if len(robots) > 1:
                winner: Optional[Robot] = None

                # check for "wait"
                for robot in robots:
                    if robot.get_next_move() == DIRECTION.WAIT:
                        winner = robot

                # the winner gets to stay, everyone else needs to go back.
                for robot in robots:
                    # move the robot back if they are not the winner
                    if robot is not winner:
                        # move robot back
                        robot
                        pass
                    # the winner is settled.
        return new_settled_entities

    def are_all_entities_settled(self, grid: Grid) -> bool:
        for _, _, entities in grid:
            robots = [entity for entity in entities if isinstance(entity, Robot)]
            if len(robots) > 1:
                return False
        return True

    # handles robot collision, or anything that needs the entire board to be moved before validation can happen.
    def correct_board_state(self, grid: Grid):
        settled_entities: List[Entity] = []
        all_entities_are_settled = False
        while not all_entities_are_settled:
            new_settled_entities = self.settle_entity_positions(grid)
            settled_entities.extend(new_settled_entities)
            if self.are_all_entities_settled(grid):
                all_entities_are_settled = True
