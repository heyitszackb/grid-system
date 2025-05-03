import pytest
from components import GridManager, Robot, Factory
from components.conveyor import Conveyor
from const import DIRECTION


class TestGridManager:
    def test_grid_manager_initialization(self):
        gm = GridManager()
        assert gm.height == 20
        assert gm.width == 20
        assert len(gm.grid) == 20
        assert all(len(row) == 20 for row in gm.grid)
        assert all(
            isinstance(cell, list) and len(cell) == 0 for row in gm.grid for cell in row
        )

    def test_grid_manager_custom_size(self):
        gm = GridManager(10, 10)
        assert gm.height == 10
        assert gm.width == 10
        assert len(gm.grid) == 10
        assert all(len(row) == 10 for row in gm.grid)

    def test_add_entity_to_location(self):
        gm = GridManager()
        robot = Robot()
        gm.add_entity_to_location(5, 5, robot)
        assert len(gm.grid[5][5]) == 1
        assert isinstance(gm.grid[5][5][0], Robot)

    def test_add_robot_out_of_bounds(self):
        gm = GridManager(5)
        robot = Robot()
        with pytest.raises(IndexError):
            gm.add_entity_to_location(5, 5, robot)

    def test_move_robot(self):
        gm = GridManager(5)
        r = Robot(
            path=[
                DIRECTION.UP,
                DIRECTION.DOWN,
                DIRECTION.LEFT,
                DIRECTION.RIGHT,
                DIRECTION.WAIT,
            ]
        )
        gm.add_entity_to_location(2, 2, r)

        # Test moving up
        gm.update()
        assert len(gm.get_entities(Robot)) == 1
        assert len(gm.grid[1][2])

        # # Test moving down
        gm.update()
        assert len(gm.grid[2][2]) == 1
        assert len(gm.grid[1][2]) == 0

        # # Test moving left
        gm.update()
        assert len(gm.grid[2][1]) == 1
        assert len(gm.grid[1][2]) == 0

        # # Test moving right
        gm.update()
        assert len(gm.grid[2][2]) == 1
        assert len(gm.grid[1][2]) == 0

    def test_multiple_robots_same_space(self):
        gm = GridManager(5)
        r1 = Robot(path=[DIRECTION.UP, DIRECTION.WAIT])
        r2 = Robot(path=[DIRECTION.WAIT, DIRECTION.DOWN])
        gm.add_entity_to_location(0, 0, r1)
        with pytest.raises(ValueError, match="You can only have one robot per cell"):
            gm.add_entity_to_location(0, 0, r2)

    def test_move_robot_out_of_bounds(self):
        gm = GridManager(5)
        r = Robot(
            path=[
                DIRECTION.UP,
                DIRECTION.DOWN,
                DIRECTION.DOWN,
                DIRECTION.DOWN,
                DIRECTION.DOWN,
                DIRECTION.DOWN,
                DIRECTION.DOWN,
            ]
        )
        gm.add_entity_to_location(0, 0, r)

        # Try to move out of bounds in each direction
        gm.update()

        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

        gm.update()
        gm.update()
        gm.update()
        gm.update()
        gm.update()
        gm.update()

        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 0
        assert len(gm.get_entities_at_location_of_type(4, 0, Robot)) == 1

    def test_wait(self):
        gm = GridManager(5)
        r = Robot(path=[DIRECTION.WAIT])
        gm.add_entity_to_location(0, 0, r)

        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

    def test_get_robots(self):
        # Initialize the GridManager and robots
        gm = GridManager(5)
        robot1 = Robot(path=[DIRECTION.WAIT])
        robot2 = Robot(path=[DIRECTION.WAIT])
        robot3 = Robot(path=[DIRECTION.WAIT])

        # Add robots to various locations
        gm.add_entity_to_location(1, 1, robot1)
        gm.add_entity_to_location(2, 2, robot2)
        gm.add_entity_to_location(3, 3, robot3)

        gm.update()

        # Call get_all_robots to fetch all robots
        robots = gm.get_entities(Robot)

        # Verify the list contains all robots added to the GridManager
        assert len(robots) == 3  # Ensure the number of robots is as expected

        # Verify no robots are duplicated in the list
        assert len(robots) == len(
            set(robots)
        )  # Check for duplicates by converting to a set

    def test_no_robot_duplicates(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.LEFT])

        gm.add_entity_to_location(0, 0, r)
        gm.update()

        robots = gm.get_entities(Robot)
        assert len(robots) == 1

    def test_get_entities_at_location_of_type(self):
        gm = GridManager()
        r1 = Robot()

        gm.add_entity_to_location(0, 0, r1)
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

    def test_get_factories_at_location(self):
        gm = GridManager()
        f1 = Factory()
        f2 = Factory()

        gm.add_entity_to_location(0, 0, f1)
        gm.add_entity_to_location(0, 1, f2)
        assert len(gm.get_entities_at_location_of_type(0, 0, Factory)) == 1
        assert len(gm.get_entities_at_location_of_type(0, 1, Factory)) == 1

    def test_get_entities_at_location(self):
        gm = GridManager()
        f = Factory()
        r = Robot()

        gm.add_entity_to_location(0, 0, r)
        gm.add_entity_to_location(0, 0, f)
        robots = len(gm.get_entities_at_location_of_type(0, 0, Robot))
        factories = len(gm.get_entities_at_location_of_type(0, 0, Factory))
        assert robots + factories == 2

    def test_update_GridManager(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.RIGHT])

        gm.add_entity_to_location(0, 0, r)

        gm.update()

        assert len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1

    def test_robot_index_should_not_change_if_they_cant_move_into_space(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.UP])

        gm.add_entity_to_location(0, 0, r)

        assert r.current_move_index == 0
        gm.update()
        robots = gm.get_entities_at_location_of_type(0, 0, Robot)
        new_r = robots[0]
        assert new_r.current_move_index == 0

    def test_robots_are_same_object_after_update(self):
        gm = GridManager()
        r = Robot()

        gm.add_entity_to_location(0, 0, r)

        gm.update()

        robots = gm.get_entities_at_location_of_type(0, 0, Robot)

        assert robots[0] == r

    def test_multiple_robots_maintain_reference_after_update(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()
        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(1, 1, r2)
        gm.update()
        robots1 = gm.get_entities_at_location_of_type(0, 0, Robot)
        robots2 = gm.get_entities_at_location_of_type(1, 1, Robot)
        assert robots1[0] == r1
        assert robots2[0] == r2

    def test_robot_moves_and_maintains_reference(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.RIGHT])
        gm.add_entity_to_location(0, 0, r)
        gm.update()
        robots = gm.get_entities_at_location_of_type(0, 1, Robot)
        assert robots[0] == r

    def test_factory_maintains_reference_after_update(self):
        gm = GridManager()
        f = Factory()
        gm.add_entity_to_location(0, 0, f)

        gm.update()

        factories = gm.get_entities_at_location_of_type(0, 0, Factory)
        assert len(factories) > 0
        assert factories[0] == f

    def test_GridManager_robots_list_contains_same_objects(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()
        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(1, 1, r2)
        gm.update()
        assert r1 in gm.get_entities(Robot)
        assert r2 in gm.get_entities(Robot)
        assert len(gm.get_entities(Robot)) == 2

    def test_multiple_updates_maintain_object_references(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.WAIT] * 5)  # Robot will stay in place for 5 updates
        gm.add_entity_to_location(0, 0, r)
        for _ in range(5):  # Perform multiple updates
            gm.update()
        robots = gm.get_entities_at_location_of_type(0, 0, Robot)
        assert robots[0] == r
        assert r in gm.get_entities(Robot)

    def test_robot_reference_maintained_after_moving(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.RIGHT, DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.UP])
        gm.add_entity_to_location(1, 1, r)

        # Move right
        gm.update()
        robots = gm.get_entities_at_location_of_type(1, 2, Robot)
        assert robots[0] == r

        # Move down
        gm.update()
        robots = gm.get_entities_at_location_of_type(2, 2, Robot)
        assert robots[0] == r

        # Move left
        gm.update()
        robots = gm.get_entities_at_location_of_type(2, 1, Robot)
        assert robots[0] == r

        # Move up
        gm.update()
        robots = gm.get_entities_at_location_of_type(1, 1, Robot)
        assert robots[0] == r

    def test_robot_reference_maintained_at_GridManager_boundary(self):
        gm = GridManager(5, 5)  # 5x5 GridManager
        r = Robot(path=[DIRECTION.RIGHT] * 5)  # Try to move right 5 times
        gm.add_entity_to_location(0, 0, r)

        for _ in range(5):
            gm.update()

        # Robot should be at the right edge of the GridManager
        robots = gm.get_entities_at_location_of_type(0, 4, Robot)
        assert robots[0] == r

    def test_add_factory_and_robot_in_same_cell(self):
        gm = GridManager(5)
        robot = Robot()
        factory = Factory()
        gm.add_entity_to_location(2, 2, robot)
        gm.add_entity_to_location(2, 2, factory)
        gm.update()

        assert len(gm.get_entities_at_location_of_type(2, 2, Robot)) == 1
        assert len(gm.get_entities_at_location_of_type(2, 2, Factory)) == 1

    def test_robot_moves_correctly_over_multiple_updates(self):
        gm = GridManager(5)
        r = Robot(path=[DIRECTION.RIGHT, DIRECTION.DOWN])

        gm.add_entity_to_location(0, 0, r)
        for _ in range(2):
            gm.update()

        assert len(gm.get_entities_at_location_of_type(1, 1, Robot)) == 1

    def test_add_multiple_factories_to_same_location(self):
        gm = GridManager(5)
        factory1 = Factory()
        factory2 = Factory()
        gm.add_entity_to_location(0, 0, factory1)
        with pytest.raises(ValueError, match="You can only have one factory per cell"):
            gm.add_entity_to_location(0, 0, factory2)

    def test_e2e_add_and_update(self):
        gm = GridManager(10)
        robot1 = Robot(path=[DIRECTION.RIGHT, DIRECTION.DOWN])
        robot2 = Robot(path=[DIRECTION.LEFT, DIRECTION.UP])
        factory = Factory()

        gm.add_entity_to_location(0, 0, robot1)
        gm.add_entity_to_location(0, 1, robot2)
        gm.add_entity_to_location(1, 0, factory)
        gm.update()  # First update

        assert (
            len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1
        )  # robot1 should move right
        assert (
            len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1
        )  # robot2 should remain in place
        assert len(gm.get_entities_at_location_of_type(1, 0, Factory)) == 1

        # Perform additional updates and check the state
        for _ in range(3):
            gm.update()
        assert (
            len(gm.get_entities_at_location_of_type(2, 2, Robot)) == 1
        )  # robot1 should move down
        assert (
            len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1
        )  # robot2 should move up

    def test_get_entities(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()

        f1 = Factory()
        f2 = Factory()
        f3 = Factory()

        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(0, 1, r2)
        gm.add_entity_to_location(0, 2, f1)
        gm.add_entity_to_location(0, 3, f2)
        gm.add_entity_to_location(0, 4, f3)

        robots = gm.get_entities(Robot)
        factories = gm.get_entities(Factory)
        all_entities = gm.get_entities()

        assert len(robots) == 2
        assert len(factories) == 3

        assert len(all_entities) == 5

    def test_add_same_entity_to_array_fails(self):
        gm = GridManager()
        r = Robot()
        r = Robot()

        gm.add_entity_to_location(0, 0, r)

        assert len(gm.get_entities()) == 1

        with pytest.raises(Exception):
            gm.add_entity_to_location(0, 1, r)

    def test_add_entity_to_GridManager(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()

        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(0, 1, r2)
        assert len(gm.entities) == 2

    def test_select_entity(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()

        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(0, 1, r2)

        gm.select_entity(r1)

        assert gm.selected_entity == r1

        gm.deselect()

        assert gm.selected_entity is None

        gm.select_entity(r2)

        assert gm.selected_entity == r2

    def test_selected_entity_removed_on_delete(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()

        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(0, 1, r2)

        gm.select_entity(r1)

        assert gm.selected_entity == r1

        gm.delete_entity(r1)

        assert gm.selected_entity is None

    def test_select_robot_not_in_GridManager_fails(self):
        gm = GridManager()
        r1 = Robot()
        r2 = Robot()

        gm.add_entity_to_location(0, 0, r2)

        assert gm.selected_entity is None

        assert not gm.select_entity(r1)

    def test_get_all_entities(self):
        gm = GridManager()
        r = Robot()
        f = Factory()

        gm.add_entity_to_location(0, 0, r)
        gm.add_entity_to_location(0, 0, f)

        assert len(gm.get_entities()) == 2

    def test_validate_entity(self):
        gm = GridManager()
        r1 = Robot()
        f1 = Factory()
        f2 = Factory()
        c1 = Conveyor()
        c2 = Conveyor()

        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(0, 0, f1)

        with pytest.raises(ValueError, match="You can only have one factory per cell"):
            gm.add_entity_to_location(0, 0, f2)

        gm.add_entity_to_location(0, 0, c1)
        with pytest.raises(ValueError, match="You can only have one conveyor per cell"):
            gm.add_entity_to_location(0, 0, c2)

    def test_conveyor_moves_right(self):
        gm = GridManager()
        r = Robot()
        c = Conveyor(direction=DIRECTION.RIGHT)

        gm.add_entity_to_location(0, 0, r)
        gm.add_entity_to_location(0, 0, c)
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1

    def test_conveyor_moves_left(self):
        gm = GridManager()
        r = Robot()
        c = Conveyor(direction=DIRECTION.LEFT)

        gm.add_entity_to_location(0, 1, r)
        gm.add_entity_to_location(0, 1, c)
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

    def test_conveyor_moves_up(self):
        gm = GridManager()
        r = Robot()
        c = Conveyor(direction=DIRECTION.UP)

        gm.add_entity_to_location(1, 0, r)
        gm.add_entity_to_location(1, 0, c)
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

    def test_conveyor_moves_down(self):
        gm = GridManager()
        r = Robot()
        c = Conveyor(direction=DIRECTION.DOWN)

        gm.add_entity_to_location(0, 0, r)
        gm.add_entity_to_location(0, 0, c)
        gm.update()
        assert len(gm.get_entities_at_location_of_type(1, 0, Robot)) == 1

    def test_conveyor_moves_in_circle(self):
        gm = GridManager()
        r = Robot()
        c1 = Conveyor(direction=DIRECTION.RIGHT)
        c2 = Conveyor(direction=DIRECTION.DOWN)
        c3 = Conveyor(direction=DIRECTION.LEFT)
        c4 = Conveyor(direction=DIRECTION.UP)

        gm.add_entity_to_location(0, 0, r)
        gm.add_entity_to_location(0, 0, c1)
        gm.add_entity_to_location(0, 1, c2)
        gm.add_entity_to_location(1, 1, c3)
        gm.add_entity_to_location(1, 0, c4)
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(1, 1, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(1, 0, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

    def test_conveyor_with_robot(self):
        gm = GridManager()
        r1 = Robot()
        c = Conveyor(direction=DIRECTION.RIGHT)

        gm.add_entity_to_location(0, 0, r1)
        gm.add_entity_to_location(0, 0, c)
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1

    def test_conveyor_with_robot_path(self):
        gm = GridManager()
        r = Robot(path=[DIRECTION.UP, DIRECTION.RIGHT])
        c1 = Conveyor(direction=DIRECTION.DOWN)
        c2 = Conveyor(direction=DIRECTION.LEFT)

        gm.add_entity_to_location(1, 0, r)
        gm.add_entity_to_location(0, 1, c1)
        gm.add_entity_to_location(1, 1, c2)

        assert len(gm.get_entities_at_location_of_type(1, 0, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(1, 1, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(1, 0, Robot)) == 1
        gm.update()
        assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1

    # def test_conveyor_with_robot_path2(self):
    #     gm =  GridManager()
    #     r1 = Robot(path=[DIRECTION.WAIT])
    #     r2 = Robot(path=[DIRECTION.LEFT])

    #     gm.add_entity_to_location(0, 0, r1)
    #     gm.add_entity_to_location(0, 1, r2)
    #     gm.update()
    #     assert len(gm.get_entities_at_location_of_type(0, 0, Robot)) == 1
    #     assert len(gm.get_entities_at_location_of_type(0, 1, Robot)) == 1
