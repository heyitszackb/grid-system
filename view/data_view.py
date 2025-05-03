from components.conveyor import Conveyor
from const import DIRECTION
from model import DataModel
from components import Robot, Factory, Entity
import pyxel
from components.entity import Resource


class DataView:
    def __init__(self):
        pass

    def draw(self, model: DataModel):
        pyxel.cls(0)
        self.draw_grid(model)
        self.draw_entities(model)
        self.draw_terminal(model)
        self.draw_stats(model)

    def draw_stats(self, model: DataModel):
        if model.is_playing:
            pyxel.text(5, 120, "Running " + "." * (model.current_tick % 3 + 1), 7)
        else:
            pyxel.text(5, 120, "paused", 7)
        pyxel.text(5, 140, "Frame " + str(model.current_frame), 7)
        pyxel.text(5, 130, "Tick " + str(model.current_tick), 7)

    def draw_terminal(self, model: DataModel):
        pyxel.text(5, 150, model.get_terminal_text(), 7)

    def draw_entities(self, model: DataModel):
        current_x = 100
        current_y = 0

        for entity in model.grid.get_entities(Entity):
            entity_type = None
            if isinstance(entity, Robot):
                entity_type = "R"
            elif isinstance(entity, Factory):
                entity_type = "F"
            elif isinstance(entity, Conveyor):
                continue

            pyxel.text(
                current_x, current_y, f"({entity.id}) {entity_type} - {entity.name}", 7
            )
            current_y += 7
            num_wood = entity.count_resource(Resource.WOOD)
            num_metal = entity.count_resource(Resource.METAL)
            num_stone = entity.count_resource(Resource.STONE)
            pyxel.text(
                current_x, current_y, f"  W:{num_wood} M:{num_metal} S:{num_stone}", 7
            )
            current_y += 7

    def draw_grid(self, model: DataModel):
        inc = 5
        for row, col, entities in model.grid:
            robots = 0
            factory = 0  # should only be one
            conveyor = 0  # should only be one
            for entity in entities:
                if isinstance(entity, Robot):
                    robots += 1
                elif isinstance(entity, Factory):
                    factory += 1
                elif isinstance(entity, Conveyor):
                    conveyor += 1
            if factory and robots:
                pyxel.text(col * inc, row * inc, "F", 7)
            elif factory and not robots:
                pyxel.text(col * inc, row * inc, "f", 7)
            elif robots == 1 and not factory:
                pyxel.text(col * inc, row * inc, "o", 7)
            elif robots and not factory:
                pyxel.text(col * inc, row * inc, "O", 7)  # more than one
            elif conveyor:
                if isinstance(entity, Conveyor):
                    direction = entity.direction
                    if direction == DIRECTION.RIGHT:
                        pyxel.text(col * inc, row * inc, ">", 7)
                    if direction == DIRECTION.LEFT:
                        pyxel.text(col * inc, row * inc, "<", 7)
                    if direction == DIRECTION.UP:
                        pyxel.text(col * inc, row * inc, "^", 7)
                    if direction == DIRECTION.DOWN:
                        pyxel.text(col * inc, row * inc, "v", 7)
