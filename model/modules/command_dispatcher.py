from .terminal_emulator import TerminalEmulator
from const import Command
from typing import Optional


class CommandDispatcher:
    def __init__(
        self,
        terminal: TerminalEmulator,
    ):
        self.terminal = terminal

    def update(self, signal: str) -> Optional[Command]:  # called each tick
        terminal_key_list = list("abcdefghijklmnopqrstuvwxyz" + "0123456789" + " ")
        if signal in terminal_key_list:
            self.terminal.add_char_to_buffer(signal)
            return None
        elif signal == "BACK":
            self.terminal.del_char_from_buffer()
            return None
        elif signal == "RIGHT":
            return Command("step")
        elif signal == "ENTER":
            command = self.terminal.get_command()
            if command.value == "play":
                return Command("play")
            elif command.value == "pause":
                return Command("pause")
            else:
                return command
        elif signal == "DELETE":
            return Command("delete")
        return None
