from components import Robot, Factory, Entity
from typing import List


# Testing class
class TestRobot:
    def test_unique_entity_id(self):
        e1 = Robot()
        e2 = Robot()
        r3 = Robot()
        f4 = Factory()
        assert e1.id == 1
        assert e2.id == 2
        assert r3.id == 3
        assert f4.id == 4
