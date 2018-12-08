'''
Stores all unique rooms in game, every type of room got its own description and features,
this is intended to be used as the building block for the dungeon generation function which
is not yet implemented

> Must-have room attributes:
NAME, USERDESC, DESC, NORTH, SOUTH, EAST, WEST, UP, DOWN, GROUND, SHOP, ENEMIES, SEEN

> Optional room attributes:
SHOPINTRO (Greetings if room is shop)
'''
# Imports package namespace which contain all constants
from dicts import *

# Returns rooms exits as a dictionary of {DIRECTION: DESTINATION, ...}
def get_room_exits(room):
    exits = {}
    for dir in DIRECTIONS:
        if room[dir]:
            exits[dir] = ROOMS[room[dir]][NAME]
        else:
            pass
            # exits[dir] = str(None)
    return exits

# USERDESC is written in the form "You ...", It explains the player's feelings and orientation from his POV (Max 2 lines)
# DESC usually starts with (The, This, There is), describing the room and its components (Min 2 lines)
# GROUND stores items on the room ground
# SHOP stores items for sale, if empty there is no shop
# ENEMIES stores enemy ids, if empty there is no combat
# SEEN tracks wether the room was seen or it is first time
ROOMS = {
    'town_square': {
        NAME: 'Town Square',
        USERDESC: 'You are in the middle of the square, you feel lost in the crowd of people.',
        DESC: 'The square is large with a fountain in the middle, narrow, paved roadss lead into all directions.',
        NORTH: 'courtyard',
        SOUTH: 'butchery',
        EAST: 'bakery',
        WEST: 'house_63',
        UP: None,
        DOWN: None,
        GROUND: ['fountain', 'evergreen', 'apple', 'bread', 'coin'],
        SHOP: [],
        ENEMIES: [],
        SEEN: False,
    },
    'house_63': {
        NAME: 'House 63 (Ground)',
        USERDESC: 'You are inside an old, deserted house. You see a dark staircase leading upwards.',
        DESC: 'This house looks like it is going to collapse.',
        NORTH: None,
        SOUTH: None,
        EAST: 'town_square',
        WEST: None,
        UP: 'house_63_1',
        DOWN: None,
        GROUND: ['coin', 'apple'],
        SHOP: [],
        ENEMIES: [],
        SEEN: False,
    },
    'house_63_1': {
        NAME: 'House 63 (Attic)',
        USERDESC: 'You are in a dark, gloomy attic, there is a staircase leading downward.',
        DESC: 'Everything is untouched, covered in dust.',
        NORTH: None,
        SOUTH: None,
        EAST: None,
        WEST: None,
        UP: None,
        DOWN: 'house_63',
        GROUND: ['dagger'],
        SHOP: [],
        ENEMIES: ['spider', 'spider'],
        SEEN: False,
    },
    'bakery': {
        NAME: 'Bakery',
        USERDESC: 'You are looking at various kinds of delicious pastry, making your stomach growl.',
        DESC: 'The air smells of warm, tasty bread.',
        NORTH: None,
        SOUTH: None,
        WEST: 'town_square',
        EAST: None,
        UP: None,
        DOWN: None,
        GROUND: [],
        SHOP: ['flatbread', 'bread', 'cake'],
        SHOPINTRO: 'The bakery has some freshly baked pastry for sale\n# Have a look:',
        ENEMIES: [],
        SEEN: False,
    },
    'butchery': {
        NAME: 'Butchery',
        USERDESC: "You are at the Butchery's entrance, You observe an old man as he sharpens his knife.",
        DESC: 'The air smells of meat and blood, it is unclean and stinky.',
        NORTH: 'town_square',
        SOUTH: None,
        EAST: None,
        WEST: None,
        UP: None,
        DOWN: None,
        GROUND: [],
        SHOP: ['beef', 'sausage'],
        SHOPINTRO: 'The butcher has some cuts ready to go\n# Have a look:',
        ENEMIES: [],
        SEEN: False,
    },
    'courtyard': {
        NAME: 'Courtyard',
        USERDESC: 'You come to a courtyard strewn with flowers, protected by small ornate cast-iron fences.',
        DESC: 'A cardinal sings, sitting atop a distant fence. You faintly make out the smell of bread, and hear voices from the south.',
        NORTH: None,
        SOUTH: 'town_square',
        EAST: None,
        WEST: None,
        UP: None,
        DOWN: None,
        GROUND: ['evergreen'],
        SHOP: [],
        ENEMIES: [],
        SEEN: False,
    }
}