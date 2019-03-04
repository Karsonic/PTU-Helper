import json
from typing import Dict, List

def _load_xp_mult(filepath: str = "data/locations.json") -> Dict[str, float]:
        """
        Loads the known xp multipliers into a dict for dynamic creation
        Locations as needed
        
        Arguments:
            filepath {[str]} -- The filpath of the .json file  

        Returns:
            Dict[str, Location] -- A dict of [lowercase location name, xp multiplier]
        """
        with open(filepath) as file:
            content = json.load(file)

        result = {}
        locations = content["locations"]

        for location in locations:
            name = location['name'].lower()
            xp_mult = location['xp_multiplier']
            result[name] = xp_mult

        return result

class Location:
    _location_xp_mults = _load_xp_mult()
    _known_locations = {}

    def __init__(self, name: str, xp_mult: int = 1):
        self.name = name
        self.xp_mult = xp_mult

    @staticmethod
    def get_from_name(name: str):
        name = name.lower()

        if name not in Location._known_locations:
            xp_mult = Location._location_xp_mults[name]
            Location._known_locations[name] = Location(name, xp_mult)
        
        return Location._known_locations[name]