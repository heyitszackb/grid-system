from components import Robot
from const import DIRECTION
import pytest


class TestRobot:
    def setup_method(self):
        # Reset the class variables before each test
        Robot.unused_names = [
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
        Robot.used_names = []

    def test_robot_creation(self):
        robot = Robot()
        assert isinstance(robot, Robot)

    def test_empty_path(self):
        robot = Robot(path=[])
        with pytest.raises(ValueError, match="Path is empty. No moves available."):
            robot.get_next_move()

    def test_single_move_path(self):
        robot = Robot(path=[DIRECTION.UP])
        assert robot.get_next_move() == DIRECTION.UP
        assert robot.get_next_move() == DIRECTION.UP
        assert robot.get_next_move() == DIRECTION.UP

    def test_multiple_moves_path(self):
        path = [DIRECTION.UP, DIRECTION.RIGHT, DIRECTION.DOWN, DIRECTION.LEFT]
        robot = Robot(path=path)

        # First cycle through the path
        assert robot.get_next_move() == DIRECTION.UP
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.RIGHT
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.DOWN
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.LEFT
        robot.update_move_index()

        # Second cycle through the path
        assert robot.get_next_move() == DIRECTION.UP
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.RIGHT
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.DOWN
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.LEFT
        robot.update_move_index()

    def test_previous_move_path(self):
        path = [DIRECTION.UP, DIRECTION.RIGHT, DIRECTION.DOWN, DIRECTION.LEFT]
        robot = Robot(path=path)

        # First cycle through the path
        assert robot.get_previous_move() == DIRECTION.LEFT
        robot.update_move_index()
        assert robot.get_previous_move() == DIRECTION.UP
        robot.update_move_index()
        assert robot.get_previous_move() == DIRECTION.RIGHT
        robot.update_move_index()
        assert robot.get_previous_move() == DIRECTION.DOWN
        robot.update_move_index()
        assert robot.get_previous_move() == DIRECTION.LEFT
        robot.update_move_index()

    def test_init_with_name(self):
        robot = Robot(name="TestBot")
        assert robot.name == "TestBot"
        assert "TestBot" not in Robot.unused_names
        assert "TestBot" not in Robot.used_names

    def test_init_without_name(self):
        robot = Robot()
        assert robot.name in Robot.used_names
        assert robot.name not in Robot.unused_names
        assert len(Robot.unused_names) == 13
        assert len(Robot.used_names) == 1

    def test_get_unique_name(self):
        names = set()
        for _ in range(14):
            name = Robot.get_unique_name()
            names.add(name)

        assert len(names) == 14
        assert "Unnamed" not in names
        assert len(Robot.unused_names) == 0
        assert len(Robot.used_names) == 14

        # Test when all names are used
        assert Robot.get_unique_name() == "Unnamed"

    def test_get_next_move(self):
        path = [DIRECTION.UP, DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.RIGHT]
        robot = Robot(path=path)

        assert robot.get_next_move() == DIRECTION.UP
        robot.update_move_index()
        assert robot.get_next_move() == DIRECTION.DOWN

    def test_update_move_index(self):
        path = [DIRECTION.UP, DIRECTION.DOWN]
        robot = Robot(path=path)

        assert robot.current_move_index == 0
        robot.update_move_index()
        assert robot.current_move_index == 1
        robot.update_move_index()
        assert robot.current_move_index == 0  # Should wrap around

    def test_set_path(self):
        path = [DIRECTION.UP, DIRECTION.DOWN]
        robot = Robot(path=path)

        assert robot.current_move_index == 0
        assert robot.get_next_move() == DIRECTION.UP

        robot.set_path([DIRECTION.DOWN, DIRECTION.UP])

        assert robot.current_move_index == 0
        assert robot.get_next_move() == DIRECTION.DOWN

        robot.update_move_index()

        assert robot.get_next_move() == DIRECTION.UP

    def test_set_path_different_length(self):
        path = [DIRECTION.WAIT, DIRECTION.WAIT, DIRECTION.WAIT, DIRECTION.RIGHT]
        robot = Robot(path=path)

        robot.update_move_index()
        robot.update_move_index()
        robot.update_move_index()

        assert robot.get_next_move() == DIRECTION.RIGHT

        assert robot.current_move_index == 3
        robot.set_path([DIRECTION.WAIT, DIRECTION.WAIT, DIRECTION.WAIT])

        assert robot.set_path([DIRECTION.WAIT, DIRECTION.WAIT, DIRECTION.WAIT])
        assert robot.current_move_index == 0

    def test_robot_path_update(self):
        robot = Robot(path=[DIRECTION.UP])
        robot.set_path([DIRECTION.DOWN])
        assert robot.get_next_move() == DIRECTION.DOWN
