from components import Robot, Factory
from components.conveyor import Conveyor
from components.entity import Entity, Resource
from components.grid import Grid
from .modules import CommandDispatcher
from const import DIRECTION, Command
from typing import Iterator, List, Optional, Deque
from collections import deque
from .utils import parse_path


class DataModel:
    def __init__(self, dispatcher: CommandDispatcher, grid: Grid):
        self.grid = grid
        self.dispatcher = dispatcher
        self.current_frame = 0
        self.delay_ms = 10  # each tick happens after x frames
        self.current_tick = 0
        self.is_playing = True
        self.signal_queue: Deque[str] = deque()

    def get_terminal_text(self) -> str:
        return self.dispatcher.terminal.buffer

    def step(self):
        self.move_entities()
        self.process_entities()

    def process_entities(self):
        # Process entities
        for _, _, entities in self.grid:
            for entity in entities:
                entity.process(entities)

    def sort_items(
        self, items: Iterator[tuple[int, int, List[Entity]]], grid: Grid
    ) -> Iterator[tuple[int, int, List[Entity]]]:
        def sort_key(item: tuple[int, int, List[Entity]]) -> tuple[bool, int, int]:
            row, col, entities = item

            robot_in_same_place = False
            for entity in entities:
                if isinstance(
                    entity, Robot
                ):  # Assuming `Robot` is the class/type for robots
                    previous_position = grid.get_coord_of_entity(entity)
                    if previous_position == (row, col):
                        robot_in_same_place = True
                        break
            return (not robot_in_same_place, row, col)

        # Convert iterator to list, sort it, and return as an iterator
        sorted_items = sorted(items, key=sort_key)
        return iter(sorted_items)

    def move_entities(self):
        tmp_grid = Grid()
        items = self.grid.get_items()
        sorted_items = self.sort_items(items, self.grid)
        for row, col, entities in sorted_items:
            for entity in entities:
                new_row, new_col = entity.move(tmp_grid, row, col, entities)
                tmp_grid.add_entity_at(new_row, new_col, entity)

        # VERIFY CORRECT TMP BOARD STATE
        # verify the new state of the board - if there is anything illegal (i.e. two robots on the same space, etc), handle it.
        self.grid.copy_entities_from(tmp_grid)

    def execute_command(self, command: Command) -> None:
        if command.value == "robot":
            row = int(command.args[0])
            col = int(command.args[1])
            # moves = [DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.DOWN]
            # random_path = [random.choice(moves) for _ in range(10)]
            r = Robot(path=[DIRECTION.WAIT])
            self.grid.add_entity_at(row, col, r)
        elif command.value == "factory":
            x = int(command.args[0])
            y = int(command.args[1])
            r_type = command.args[2]
            if r_type == "wood":
                f = Factory(resource_type=Resource.WOOD)
                self.grid.add_entity_at(x, y, f)
            if r_type == "metal":
                f = Factory(resource_type=Resource.METAL)
                self.grid.add_entity_at(x, y, f)
            if r_type == "stone":
                f = Factory(resource_type=Resource.STONE)
                self.grid.add_entity_at(x, y, f)
        elif command.value == "conveyor":
            x = int(command.args[0])
            y = int(command.args[1])
            conveyor_direction = command.args[2]
            if conveyor_direction == "up":
                c = Conveyor(direction=DIRECTION.UP)
                self.grid.add_entity_at(x, y, c)
            if conveyor_direction == "down":
                c = Conveyor(direction=DIRECTION.DOWN)
                self.grid.add_entity_at(x, y, c)
            if conveyor_direction == "left":
                c = Conveyor(direction=DIRECTION.LEFT)
                self.grid.add_entity_at(x, y, c)
            if conveyor_direction == "right":
                c = Conveyor(direction=DIRECTION.RIGHT)
                self.grid.add_entity_at(x, y, c)
        elif command.value == "step":
            self.step()
        elif command.value == "delete":
            entity_id = int(command.args[0])
            entity = self.grid.get_entity_by_id(entity_id)
            if entity:
                self.grid.remove_entity(entity)
        elif command.value == "play":
            self.is_playing = True
        elif command.value == "pause":
            self.is_playing = False
            print("paused")
        elif command.value == "move":
            entity_id = int(command.args[0])
            direction = command.args[1]
            entity = self.grid.get_entity_by_id(entity_id)
            if entity:
                if direction == "right":
                    self.grid.move_entity_in_direction(entity, DIRECTION.RIGHT)
                elif direction == "left":
                    self.grid.move_entity_in_direction(entity, DIRECTION.LEFT)
                elif direction == "up":
                    self.grid.move_entity_in_direction(entity, DIRECTION.UP)
                elif direction == "down":
                    self.grid.move_entity_in_direction(entity, DIRECTION.DOWN)
        elif command.value == "set":
            specific_set_command = command.args[0]
            if specific_set_command == "path":
                entity_id = int(command.args[1])
                str_path = command.args[2]
                parsed_path = parse_path(str_path)
                entity = self.grid.get_entity_by_id(entity_id)
                if isinstance(entity, Robot):
                    entity.set_path(parsed_path)

    # called 60 times / second
    def update(self, signal: Optional[str]) -> None:
        if self.current_frame == 0:
            self.run_seed()
        self.current_frame += 1
        if signal:
            self.signal_queue.append(signal)

        if self.current_frame % self.delay_ms == 0:
            self.current_tick += 1
            if self.is_playing:
                self.execute_command(Command("step"))
            if self.signal_queue:
                current_signal = self.signal_queue.popleft()
                if current_signal:
                    command = self.dispatcher.update(current_signal)
                    if command:
                        self.execute_command(command)

    def run_seed(self):
        self.execute_command(Command("conveyor 5 5 right"))
        self.execute_command(Command("conveyor 5 6 right"))
        self.execute_command(Command("conveyor 5 7 right"))
        self.execute_command(Command("conveyor 5 8 right"))
        self.execute_command(Command("conveyor 5 9 right"))

        self.execute_command(Command("conveyor 5 10 down"))
        self.execute_command(Command("conveyor 6 10 down"))
        self.execute_command(Command("conveyor 7 10 down"))
        self.execute_command(Command("conveyor 8 10 down"))

        self.execute_command(Command("conveyor 9 10 left"))
        self.execute_command(Command("conveyor 9 9 left"))
        self.execute_command(Command("conveyor 9 8 left"))

        # self.execute_command(Command("robot 5 5"))
        # self.execute_command(Command("set path 13 lllluuuuwwwwrrrr"))
