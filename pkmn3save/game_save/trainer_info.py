import enum
import struct
from pkmn3save.mapping import BinaryChunk
from pkmn3save.data_types.strings import to_ascii

import typing
if typing.TYPE_CHECKING:
    from . import GameSave

SECTION_ID = 0
NAME = BinaryChunk(0x0, 7)
GENDER = BinaryChunk(0x8, 1)
GAME_CODE = BinaryChunk(0x00AC, 4)


class GameCode(enum.Enum):
    RUBY_SAPPHIRE = 0x00000000
    FIRERED_LEAFGREEN = 0x00000001
    EMERALD = None


class Gender(enum.Enum):
    BOY = 0x00
    GIRL = 0x01


class TrainerInfo:
    def __init__(self, data: bytes):
        self.data = data

    @classmethod
    def from_game_save(cls, save: 'GameSave'):
        return cls(save.sections[SECTION_ID])

    @property
    def name(self) -> str:
        return to_ascii(NAME(self.data))

    @property
    def gender(self) -> Gender:
        return Gender(GENDER(self.data)[0])

    @property
    def game_code(self) -> GameCode:
        data = GAME_CODE(self.data)
        num = struct.unpack("L", data)
        try:
            return GameCode(num)
        except ValueError:
            return GameCode.EMERALD

    def __str__(self):
        return f"TrainerInfo(name={self.name}, gender={self.gender}, game_code={self.game_code})"
