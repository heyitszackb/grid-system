from model.modules.terminal_emulator import TerminalEmulator


class TestTerminalEmulator:
    def setup_method(self):
        self.terminal = TerminalEmulator()

    def test_initialization(self):
        assert self.terminal.buffer == ""

    def test_add_char_to_buffer(self):
        self.terminal.add_char_to_buffer("a")
        assert self.terminal.buffer == "a"
        self.terminal.add_char_to_buffer("b")
        assert self.terminal.buffer == "ab"

    def test_del_char_from_buffer(self):
        self.terminal.add_char_to_buffer("a")
        self.terminal.add_char_to_buffer("b")
        self.terminal.del_char_from_buffer()
        assert self.terminal.buffer == "a"
        self.terminal.del_char_from_buffer()
        assert self.terminal.buffer == ""

    def test_del_char_from_empty_buffer(self):
        self.terminal.del_char_from_buffer()
        assert self.terminal.buffer == ""

    def test_clear_buffer(self):
        self.terminal.add_char_to_buffer("test")
        self.terminal.clear_buffer()
        assert self.terminal.buffer == ""
