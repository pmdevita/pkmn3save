from gen3editor.mapping import GAME_SAVE_A, GAME_SAVE_B, BinaryChunk
from .trainer_info import TrainerInfo, GameCode
from .team_items import TeamItems, TeamItemsLGFR

SECTION_ID = BinaryChunk(0x0FF4, 1)
CHECKSUM = BinaryChunk(0x0FF6, 2)
SIGNATURE = BinaryChunk(0x0FF8, 4)
SAVE_INDEX = BinaryChunk(0x0FFC, 4)

SECTION_SIZE = 4096


class GameSave:
    def __init__(self, data: bytes):
        self.data = data
        assert len(self.data) == GAME_SAVE_A.size
        self.sections = GameSaveSections(self)

    @classmethod
    def game_a_from_save_file(cls, data: bytes) -> 'GameSave':
        return cls(GAME_SAVE_A(data))

    @classmethod
    def game_b_from_save_file(cls, data: bytes) -> 'GameSave':
        return cls(GAME_SAVE_B(data))

    @property
    def trainer_info(self) -> TrainerInfo:
        return TrainerInfo.from_game_save(self)

    @property
    def team_items(self) -> TeamItems:
        if self.trainer_info.game_code == GameCode.FIRERED_LEAFGREEN:
            return TeamItemsLGFR.from_game_save(self)
        else:
            return TeamItems.from_game_save(self)

    def __str__(self):
        return str(self.trainer_info)


class GameSaveSections:
    def __init__(self, game_save: GameSave):
        self.game_save = game_save
        self.section_map = self.map_sections()

    def map_sections(self):
        map = {}
        for i in range(14):
            section_start = i * SECTION_SIZE
            section = self.game_save.data[section_start: section_start + SECTION_SIZE]
            section_id = SECTION_ID(section)
            map[int(section_id[0])] = i
        return map

    def __getitem__(self, item):
        location = self.section_map[item]
        start = location * SECTION_SIZE
        return self.game_save.data[start: start + SECTION_SIZE]
