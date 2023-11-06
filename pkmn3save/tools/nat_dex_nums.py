from pathlib import Path
import requests


csv = Path(__file__).parent.parent / "data" / "pokemon.csv"

lines = []
with open(csv, "r") as f:
    for line in f.readlines():
        parts = line.strip().split(",")
        if parts[1] == "" and "?" not in parts[2]:
            try:
                r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{parts[2].lower()}")
                j = r.json()
                parts[1] = str(j["id"])
            except:
                print("Couldn't find", parts[2])
        lines.append(",".join(parts))

with open(csv, "w", encoding="utf8") as f:
    f.write("\n".join(lines))
