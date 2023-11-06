# Pokémon Gen 3 Save ~~Editor~~ Reader

Very unfinished but well planned (I think), slightly useful library for reading save data from 

- Pokémon Ruby
- Pokémon Sapphire
- Pokémon Leaf Green
- Pokémon Fire Red
- Pokémon Emerald

PRs welcome to add missing functionality.

## Install

```
pip install git+https://github.com/pmdevita/pkmn3save
```

## Usage

There are no docs but stuff is typed so your IDE should help you fumble through it.

```python
from pkmn3save import SaveFile

data = SaveFile("emerald.sav")

print(data.game_save_a.trainer_info)

print(data.game_save_a.team_items.team)


```


## Reference

Library built using the [Bulbapedia article as a reference](https://m.bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_III)#Section_1_-_team_.2F_items)
Thanks to the authors!
