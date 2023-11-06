from pathlib import Path

CSV = Path(__file__).parent / "pokemon.csv"

# Map National Dex to gen 3 data
NAT_DEX = {}

# Map gen 3 Pokemon data index to national dex
INDEX = []

with open(CSV, "r") as f:
    for line in f.readlines():
        parts = line.strip().split(",")
        INDEX.append((parts[1], parts[2]))
        try:
            NAT_DEX[int(parts[1])] = int(parts[0])
        except ValueError:
            pass


class PokemonSpecies:
    def __init__(self, index_id: int):
        self.index = index_id
        self.nat_dex, self.name = INDEX[index_id]

    @classmethod
    def from_gen_3(cls, index_id) -> 'PokemonSpecies':
        return cls(index_id)

    @classmethod
    def from_nat_dex(cls, nat_dex: int) -> 'PokemonSpecies':
        return cls(NAT_DEX[nat_dex])

    def __str__(self) -> str:
        return f"{self.nat_dex}-{self.name}"

    def __repr__(self):
        return str(self)
