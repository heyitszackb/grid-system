from typing import List
from const import DIRECTION


def parse_path(str_path: str) -> List[DIRECTION]:
    direction_map = {
        "r": DIRECTION.RIGHT,
        "l": DIRECTION.LEFT,
        "u": DIRECTION.UP,
        "d": DIRECTION.DOWN,
        "w": DIRECTION.WAIT,
    }

    return [direction_map[char] for char in str_path.lower() if char in direction_map]
