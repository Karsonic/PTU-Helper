import json
from level import Level
from location import Location
from pokemon import Pokemon
from typing import Any, Callable, List

pk_json_file = 'data/pokemon.json'


def _confirm(msg: str) -> bool:
    print(msg)
    confirm = input('Is this correct? [y/yes]').lower()
    return confirm in ['y', 'yes', '']


def _prompt_location() -> Location:
    loc_name = input('Enter the location of the pokemon: ').lower()
    if loc_name not in Location._known_locations:
        xp_mult = float(input('Add an xp multiplier for this new location: '))
        return Location.add_new_location(loc_name, xp_mult)
    else:
        return Location.get_from_name(loc_name)


def _prompt_name() -> str:
    return input('Enter a name: ')


def _prompt_index(msg: str, iterable: List[Any]) -> int:
    def in_range(index: int):
        return 0 <= index < len(iterable)

    while True:
        try:
            index = int(input(msg))
        except ValueError:
            print('Please enter an integer...')
            continue
        
        if in_range(index):
            return index
        else:
            print('Out of range, try again...')
    

def p_add_xp(pokemons: List[Pokemon]) -> None:
    try:
        xp = int(input('Enter the amount of xp earned: '))
        xp = max(xp, 0)
    except ValueError:
        print('Invalid xp amount. Please specify an integer')
        return

    if not _confirm(f'Will add {xp} xp'):
        return

    for pokemon in pokemons:
        levelup_count = pokemon.add_xp(xp)
        if levelup_count > 0:
            print(f'{pokemon.name} leveled up {levelup_count} times to lvl {pokemon.level.number}')


def p_create_pokemon(pokemons: List[Pokemon]) -> None:
    try:
        name = _prompt_name()
        location = _prompt_location()
        xp = int(input('Enter the starting xp of the pokemon: '))
        level = Level(xp)
    except:
        print('Failed to create pokemon')
        return
    
    if _confirm(f'Will create {name}, with {xp} xp, located in {location.name}'):
        pokemon = Pokemon(name, location, level)
        pokemons.append(pokemon)
        print(f'Created {pokemon}')


def p_list_pokemon(pokemons: List[Pokemon]) -> None:
    for idx, pokemon in enumerate(pokemons):
        print(f'{idx}) {pokemon}')


def p_move_pokemon(pokemons: List[Pokemon]) -> None:
    index = _prompt_index('Enter the pokemon # you wish to move: ', pokemons)
    location = _prompt_location()

    if _confirm(f'Will move {pokemons[index].name} to {location.name}'):
        pokemons[index].location = location


def p_remove_pokemon(pokemons: List[Pokemon]) -> None:
    index = _prompt_index('Enter the pokemon # you wish to remove: ', pokemons)

    if _confirm(f'Will delete {pokemons[index].name}. THERE IS PERMANENT.'):
        del pokemons[index]


def p_rename_pokemon(pokemons: List[Pokemon]) -> None:
    index = _prompt_index('Enter the pokemon # you wish to rename: ', pokemons)
    name = _prompt_name()

    if _confirm(f'Will rename {pokemons[index].name} to {name}'):
        pokemons[index].name = name


def p_quit(pokemons: List[Pokemon]) -> None:
    print('Saving...')
    try:
        Pokemon.save_pokemon(pokemons, pk_json_file)
        Location.save()
    except Exception as ex:
        print(f'Failed to save: {ex}')
    finally:
        print('Exiting...')
        exit(0)
    

options = {
    0: ('List pokemon', p_list_pokemon),
    1: ('Add xp', p_add_xp),
    2: ('Create a pokemon', p_create_pokemon),
    3: ('Move a pokemon', p_move_pokemon), 
    4: ('Rename a pokemon', p_rename_pokemon),
    5: ('Save and Quit', p_quit)
}

def prompt(pokemons: List[Pokemon]) -> None:
    print()
    print('Options:')
    
    for index in options:
        print(f'{index}) {options[index][0]}')
    
    choice = _prompt_index('', options)
    print()
    options[choice][1](pokemons)


if __name__ == "__main__":
    pokemons = Pokemon.load_pokemon(pk_json_file)
    
    print(f'Loaded the following pokemon from {pk_json_file}')
    for pokemon in pokemons:
        print(pokemon)

    while True:
        prompt(pokemons)