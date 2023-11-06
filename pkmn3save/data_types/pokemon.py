import enum
import struct
from functools import cached_property

from pkmn3save.mapping import BinaryChunk, StructChunk, DataMapping
from pkmn3save.data.pokemon import PokemonSpecies

PERSONALITY = BinaryChunk(0, 4)
OT_ID = BinaryChunk(4, 4)
PKMN_DATA = BinaryChunk(32, 48)

SPECIES = StructChunk("H", 0, 2)
POKERUS = StructChunk("B", 0, 1)

HP_EV = BinaryChunk(0, 1)
ATTACK_EV = BinaryChunk(1, 1)


class PokemonDataSubsection(enum.Enum):
    GROWTH = "G"
    ATTACKS = "A"
    EVS_CONDITION = "E"
    MISCELLANEOUS = "M"


def generate_substructure_map():
    sections = ["G", "A", "E", "M"]
    return iterate_sub("", sections)


def iterate_sub(word: str, letters: list[str]):
    results = []
    if len(letters) == 1:
        return [word + letters[0]]

    for i in letters:
        new_list = letters[:]
        new_list.remove(i)
        results.extend(iterate_sub(word + i, new_list))
    return results


GAME_SUBSECTIONS = generate_substructure_map()


def personality_to_subsections(personality: int) -> list[PokemonDataSubsection]:
    id = personality % 24
    return [PokemonDataSubsection(i) for i in GAME_SUBSECTIONS[id]]


class Pokemon(DataMapping):
    def __init__(self, data: bytes):
        super().__init__(data)
        self.pkmn_data = PokemonData(self.personality, self.original_trainer_id, PKMN_DATA(self.data))

    @cached_property
    def personality(self) -> int:
        data = PERSONALITY(self.data)
        return struct.unpack("I", data)[0]

    @cached_property
    def original_trainer_id(self) -> int:
        data = OT_ID(self.data)
        return struct.unpack("I", data)[0]

    @cached_property
    def species(self) -> PokemonSpecies:
        data = self.pkmn_data.get_section(PokemonDataSubsection.GROWTH)
        index = SPECIES(data)
        return PokemonSpecies.from_gen_3(index)

    @cached_property
    def pokerus(self) -> bool:
        return POKERUS(self.pkmn_data.get_section(PokemonDataSubsection.MISCELLANEOUS)) == 1

    @cached_property
    def hp_ev(self) -> int:
        return HP_EV(self.pkmn_data.get_section(PokemonDataSubsection.EVS_CONDITION))[0]

    @cached_property
    def attack_ev(self) -> int:
        return ATTACK_EV(self.pkmn_data.get_section(PokemonDataSubsection.EVS_CONDITION))[0]

    def __str__(self):
        return f"Pokemon(species={self.species}, hp_ev={self.hp_ev}, attack_ev={self.attack_ev})"

    def __repr__(self):
        return str(self)


class PokemonData(DataMapping):
    def __init__(self, personality: int, trainer_id: int, data: bytes):
        super().__init__(data)
        self.personality = personality
        self.trainer_id = trainer_id
        self.section_map = personality_to_subsections(personality)
        self.decrypted_data = bytes()
        for i in range(48 // 4):
            start = i * 4
            end = start + 4
            data_chunk = self.data[start: end]
            chunk = struct.unpack("I", data_chunk)[0]
            xored = chunk ^ self.encryption_key
            self.decrypted_data += struct.pack("I", xored)

    @cached_property
    def encryption_key(self):
        return self.trainer_id ^ self.personality

    def get_section(self, section: PokemonDataSubsection) -> bytes:
        index = self.section_map.index(section)
        start = index * 12
        end = start + 12
        return self.decrypted_data[start: end]

    def __getitem__(self, item: PokemonDataSubsection) -> bytes:
        return self.get_section(item)



a = PokemonData()




