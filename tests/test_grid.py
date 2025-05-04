from components.conveyor import Conveyor
from components.factory import Factory
from components.grid import Coord, Grid
from components.robot import Robot
import pytest

from const import DIRECTION


class TestGrid:
    def test_no_duplicates_same_position(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        with pytest.raises(ValueError):
            g.add_entity_at(1, 1, r)

    def test_no_duplicates_different_position(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        with pytest.raises(ValueError):
            g.add_entity_at(1, 2, r)

    def test_add_entity_updates_locations(self):
        g = Grid()
        r1 = Robot()
        r3 = Robot()
        g.add_entity_at(1, 1, r1)
        assert g._entities_at_coord[Coord(1, 1)] == [r1]

        g.add_entity_at(1, 2, r3)
        assert g._entities_at_coord[Coord(1, 2)] == [r3]

    def test_add_entity_updates_positions(self):
        g = Grid()
        r1 = Robot()
        g.add_entity_at(1, 1, r1)
        assert g._coord_of_entity[r1] == Coord(1, 1)

    # get entities at
    def test_get_entities_at_empty(self):
        g = Grid()
        assert g.get_entities_at(1, 1) == []

    def test_get_entities_at_with_entities(self):
        g = Grid()
        r1 = Robot()
        c1 = Conveyor()
        g.add_entity_at(1, 1, r1)
        g.add_entity_at(1, 1, c1)
        assert g.get_entities_at(1, 1) == [r1, c1]

    # add entity at
    def test_add_entity_at_new_coord(self):
        g = Grid()
        r = Robot()
        assert g.add_entity_at(1, 1, r) is True
        assert g.get_entities_at(1, 1) == [r]
        assert g._coord_of_entity[r] == Coord(1, 1)

    def test_add_entity_at_existing_coord(self):
        g = Grid()
        r1 = Robot()
        c1 = Conveyor()
        g.add_entity_at(1, 1, r1)
        g.add_entity_at(1, 1, c1)
        assert g.get_entities_at(1, 1) == [r1, c1]
        assert g._coord_of_entity[r1] == Coord(1, 1)
        assert g._coord_of_entity[c1] == Coord(1, 1)

    def test_add_entity_at_raises_value_error_on_duplicate(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        with pytest.raises(ValueError):
            g.add_entity_at(1, 2, r)

    # remove entity
    def test_remove_entity_success(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        assert g.remove_entity(r) is True
        assert g.get_entities_at(1, 1) == []
        assert r not in g._coord_of_entity

    def test_remove_entity_not_in_grid(self):
        g = Grid()
        r = Robot()
        assert g.remove_entity(r) is False

    def test_remove_entity_clears_coord(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        g.remove_entity(r)
        assert Coord(1, 1) not in g._entities_at_coord

    # test move
    def test_move_entity_success(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        assert g.move_entity(2, 2, r) is True
        assert g.get_entities_at(1, 1) == []
        assert g.get_entities_at(2, 2) == [r]
        assert g._coord_of_entity[r] == Coord(2, 2)

    def test_move_entity_not_in_grid(self):
        g = Grid()
        r = Robot()
        assert g.move_entity(1, 1, r) is False
        assert r not in g._coord_of_entity

    def test_move_entity_to_same_location(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        assert g.move_entity(1, 1, r) is True
        assert g.get_entities_at(1, 1) == [r]
        assert g._coord_of_entity[r] == Coord(1, 1)

    # iter
    def test_iter_empty_grid(self):
        g = Grid()
        assert list(iter(g)) == []

    def test_iter_with_entities(self):
        g = Grid()
        r1 = Robot()
        r2 = Robot()
        r3 = Robot()
        g.add_entity_at(1, 1, r1)
        g.add_entity_at(1, 2, r2)
        g.add_entity_at(2, 2, r3)

        result = list(iter(g))
        expected = [(1, 1, [r1]), (1, 2, [r2]), (2, 2, [r3])]
        assert result == expected

    def test_get_coord_of_entity(self):
        g = Grid()
        r1 = Robot()
        r2 = Robot()

        # Add entities to the grid
        g.add_entity_at(1, 1, r1)
        g.add_entity_at(2, 2, r2)

        # Test that the coordinates are retrieved correctly as tuples
        assert g.get_coord_of_entity(r1) == (1, 1)
        assert g.get_coord_of_entity(r2) == (2, 2)

        # Test that an entity not in the grid returns None
        r3 = Robot()
        assert g.get_coord_of_entity(r3) is None

    # get entity by id
    def test_get_entity_by_id_existing(self):
        g = Grid()
        r1 = Robot()
        r1.id = 1
        g.add_entity_at(1, 1, r1)

        assert g.get_entity_by_id(1) == r1

    def test_get_entity_by_id_non_existent(self):
        g = Grid()
        r1 = Robot()
        r1.id = 1
        g.add_entity_at(1, 1, r1)

        assert g.get_entity_by_id(2) is None

    def test_add_delete_entity_by_id(self):
        g = Grid()
        r = Robot()
        # Assuming Robot has an id attribute
        r.id = 1
        g.add_entity_at(1, 1, r)

        # Verify that the entity can be found by its ID
        assert g.get_entity_by_id(1) == r

        # Remove the entity
        g.remove_entity(r)

        # Verify that the entity cannot be found by its ID
        assert g.get_entity_by_id(1) is None

    # test movement
    def test_move_entity_in_direction_success(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)

        # Move up
        assert g.move_entity_in_direction(r, DIRECTION.UP) is True
        assert g.get_coord_of_entity(r) == (0, 1)

        # Move right
        assert g.move_entity_in_direction(r, DIRECTION.RIGHT) is True
        assert g.get_coord_of_entity(r) == (0, 2)

        # Move down
        assert g.move_entity_in_direction(r, DIRECTION.DOWN) is True
        assert g.get_coord_of_entity(r) == (1, 2)

        # Move left
        assert g.move_entity_in_direction(r, DIRECTION.LEFT) is True
        assert g.get_coord_of_entity(r) == (1, 1)

    # test validate entity
    def test_validate_entity_new_entity(self):
        g = Grid()
        r = Robot()
        c = Coord(1,1)
        assert g._validate_entity(c, r) is True

    def test_validate_entity_existing_entity(self):
        g = Grid()
        r = Robot()
        g.add_entity_at(1, 1, r)
        with pytest.raises(ValueError, match="Entity .* already exists in the grid."):
            c = Coord(2,2)
            g._validate_entity(c, r)

    def test_validate_entity_multiple_robots(self):
        g = Grid()
        r1 = Robot()
        r2 = Robot()
        g.add_entity_at(1, 1, r1)
        with pytest.raises(ValueError, match="You can only have one Robot per cell"):
            c = Coord(1,1)
            g._validate_entity(c, r2)

    def test_validate_entity_multiple_conveyors(self):
        g = Grid()
        c1 = Conveyor()
        c2 = Conveyor()
        g.add_entity_at(1, 1, c1)
        with pytest.raises(ValueError, match="You can only have one Conveyor per cell"):
            c = Coord(1,1)
            g._validate_entity(c, c2)

    def test_validate_entity_multiple_factories(self):
        g = Grid()
        f1 = Factory()
        f2 = Factory()
        g.add_entity_at(1, 1, f1)
        with pytest.raises(ValueError, match="You can only have one Factory per cell"):
            c = Coord(1,1)
            g._validate_entity(c, f2)

    def test_validate_entity_different_types_same_cell(self):
        g = Grid()
        r = Robot()
        c = Conveyor()
        f = Factory()
        xy = Coord(1,1)
        assert g._validate_entity(xy, r) is True
        assert g._validate_entity(xy, c) is True
        assert g._validate_entity(xy, f) is True

    def test_validate_entity_same_type_different_cells(self):
        g = Grid()
        r1 = Robot()
        r2 = Robot()
        assert g._validate_entity(Coord(1,1), r1) is True
        assert g._validate_entity(Coord(2,2), r2) is True
