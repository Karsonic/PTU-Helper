import json
from typing import Dict

def _load_levels(filepath: str = "data/levels.json") -> Dict[int, int]:
        """Loads the levels json file into a dict
        
        Arguments:
            filepath {[str]} -- The filpath of the .json file  

        Returns:
            Dict[int, Level] -- A dict of [level number, min xp for level]
        """
        with open(filepath) as file:
            content = json.load(file)

        result = {}
        levels = content["levels"]

        for level in levels:
            level_num = int(level)
            level_xp = levels[level]
            result[level_num] = level_xp

        return result

class Level:
    """A class for dealing with levels and leveling up"""
    _level_lookup = _load_levels()

    def __init__(self, xp: int):
        self.xp = xp
        self.number = Level.get_level_number(xp)

    def get_next_level_xp(self) -> int:
        """Gets the xp requirement for the next level
        
        Returns:
            int -- [description]
        """
        if self.number >= 100:
            return 999999 # TODO: Handle better
        return Level._level_lookup[self.number + 1] 

    def add_xp(self, xp: int) -> int:
        """
        Add experience to the Level, and returns whether this caused the level
        to increase
        
        Arguments:
            xp {[int]} -- An amount of experience (after any modifiers)

        Returns:
            int -- The number of levels gained, 0 if none are gained
        """
        self.xp += xp
        levels_gained = 0

        while self.xp >= self.get_next_level_xp():
            self.number += 1
            levels_gained += 1

        return levels_gained
            
    @staticmethod
    def get_level_number(xp: int) -> int:
        """Gets the level number corresponding to the provided xp amount
        
        Arguments:
            xp {int} -- An amount of experience
        
        Returns:
            int -- The level number of something with the provided amount of xp
        """
        return next((level for level in Level._level_lookup if Level._level_lookup[level] > xp))