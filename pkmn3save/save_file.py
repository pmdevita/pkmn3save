import typing
from pathlib import Path
from .game_save import GameSave
from .hall_of_fame import HallOfFame


class SaveFile:
    def __init__(self, file: str | Path | typing.IO):
        if isinstance(file, str) or isinstance(file, Path):
            with open(file, "rb") as f:
                self.data = f.read()
        else:
            self.data = file.read()

    @property
    def game_save_a(self) -> GameSave:
        return GameSave.game_a_from_save_file(self.data)

    @property
    def game_save_b(self) -> GameSave:
        return GameSave.game_b_from_save_file(self.data)

    @property
    def hall_of_fame(self):
        return HallOfFame.from_save_file(self.data)

    def __str__(self):
        return str(self.game_save_a)


