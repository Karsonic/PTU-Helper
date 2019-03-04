from enum import Enum, auto
import json
from level import Level
from location import Location
from typing import Dict, List

class Pokemon:
    """A pokemon and its experience information"""
    def __init__(self, name: str, location: Location, level: Level = Level(0)):
        self.level = level
        self.location = location
        self.name = name

    def add_xp(self, xp: int) -> bool:
        """
        Add a raw experience amount before considering multiplier and returns
        whether or not it caused a level-up.
        
        Returns:
            bool -- True if this experience caused a level-up, False otherwise
        """
        return self.level.add_xp(xp * self.location.xp_mult)

    @staticmethod
    def load_pokemon(filepath: str = 'data/pokemon.json') -> List['Pokemon']:
        with open(filepath, 'r') as f:
            content = json.load(f)
        
        result = []
        pokemons = content["pokemons"]

        for pokemon in pokemons:
            name = pokemon['name']
            loc_name = pokemon['location']
            location = Location.get_from_name(loc_name)
            level = Level(pokemon['xp'])
            result.append(Pokemon(name, location, level))

        return result

    def __repr__(self):
        return f'A level {self.level} pokemon named "{self.name}" ' + \
               f'with ({self.level.xp} / {self.level.get_next_level_xp}) experience points'