# robots

Currently a WIP, however main should always be functioning.
I love systems, so I am working on creating a game where the player needs to create a system of autonomous robots to complete goals, build more robots, and make a bigger and better system. Inspired by Factorio and Minecraft, and mostly for my personal coding joy.
My vision for this projects includes:
- Programmable robots
- Many building types
- Beautiful aesthetics (way down the line...)
- Resource collection
- ...and more!

### Setup instructions
1. Inside of `Robot` directory: `pip install pyxel`.
2. Run `pyxel run main.py`

### Changelog:
- Added feature: Deselect entity, `deselect`. If there is an entity currently selected, this command deselects it.
- Added feature: Select entity `select x`, where x is the entity ID.
- Added feature: Add robot/factory to cell (type `robot x y` or `factory x y` and press enter to create a robot or factory at `x, y` in the grid).
- Added: README.md
- Added: .gitignore
- Added feature: robot command (type `robot` and press enter to create a robot)
- Added feature: factory command (type `factory` and press enter to create a factory)