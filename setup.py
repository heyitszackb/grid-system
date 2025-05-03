# model
from components.grid import Grid
from model.data_model import DataModel
from model.modules.command_dispatcher import CommandDispatcher
from model.modules.terminal_emulator import TerminalEmulator

# view
from view.data_view import DataView

# controller
from controller import Controller


# setup
class ControllerFactory:
    def __init__(self):
        # model
        self.terminal = TerminalEmulator()
        self.dispatcher = CommandDispatcher(self.terminal)
        self.grid = Grid()
        self.model = DataModel(self.dispatcher, self.grid)

        # view
        self.view = DataView()

        # controller
        self.controller = Controller(self.model, self.view)

    def create_controller(self):
        return self.controller
