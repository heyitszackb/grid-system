from typing import Optional
from model import DataModel
from view import DataView
import pyxel


class Controller:
    def __init__(self, data_model: DataModel, data_view: DataView):
        self.setup_pyxel()
        self.data_model = data_model
        self.data_view = data_view

    def setup_pyxel(self) -> None:
        pyxel.init(200, 200, fps=120)
        pyxel.mouse(visible=True)
        # pyxel.load('tilemap_file.pyxres')

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        signal = self.process_keys()
        self.data_model.update(signal)

    def draw(self):
        self.data_view.draw(self.data_model)

    def process_keys(self) -> Optional[str]:
        terminal_keys = (
            list(range(pyxel.KEY_A, pyxel.KEY_Z + 1))
            + list(range(pyxel.KEY_0, pyxel.KEY_9 + 1))
            + [pyxel.KEY_SPACE]
        )

        for key in terminal_keys:
            if pyxel.btnp(key):
                return chr(key)

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            return "BACK"
        if pyxel.btnp(pyxel.KEY_RETURN):
            return "ENTER"
        if pyxel.btnp(pyxel.KEY_RIGHT):
            return "RIGHT"
        if pyxel.btnp(pyxel.KEY_DELETE):
            return "DELETE"
        return None
