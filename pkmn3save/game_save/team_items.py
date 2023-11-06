import struct
from functools import cached_property

from gen3editor.mapping import BinaryChunk, DataMapping
from gen3editor.data_types.pokemon import Pokemon

import typing
if typing.TYPE_CHECKING:
    from . import GameSave


SECTION_ID = 1


class TeamItems(DataMapping):
    _TEAM_SIZE = BinaryChunk(0x0234, 4)
    _POKEMON_LIST = BinaryChunk(0x0238, 600)

    @classmethod
    def from_game_save(cls, save: 'GameSave'):
        return cls(save.sections[SECTION_ID])

    @cached_property
    def team_size(self) -> int:
        data = self._TEAM_SIZE(self.data)
        num = struct.unpack("L", data)
        return num[0]

    @cached_property
    def team(self) -> list[Pokemon]:
        team_data = self._POKEMON_LIST(self.data)
        team = []
        for i in range(self.team_size):
            start = 100 * i
            end = start + 100
            team.append(Pokemon(team_data[start: end]))
        return team


class TeamItemsLGFR(TeamItems):
    _TEAM_SIZE = BinaryChunk(0x0034, 4)
    _POKEMON_LIST = BinaryChunk(0x0038, 600)

