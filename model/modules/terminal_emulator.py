from const import Command


class TerminalEmulator:
    def __init__(self) -> None:
        self.buffer: str = ""

    def add_char_to_buffer(self, char: str) -> None:
        self.buffer += char

    def del_char_from_buffer(self) -> None:
        self.buffer = self.buffer[:-1]

    def clear_buffer(self) -> None:
        self.buffer = ""

    def get_command(self) -> Command:
        command = Command(self.buffer)
        self.clear_buffer()
        return command
