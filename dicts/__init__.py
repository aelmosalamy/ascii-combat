'''
Stores all constants needed for our dict files to work properly, stores window size, 
tags to be displayed in inventory, bullets and separators and dict keys.
'''
import colorama as C

# General color constants
HIGHLIGHT_COLOR = C.Fore.MAGENTA
CYAN = C.Fore.CYAN
WHITE = C.Fore.WHITE
RED = C.Fore.RED
BRIGHT = C.Style.BRIGHT
DIM = C.Style.NORMAL
# This is the list of tags to be displayed in inventory
INVENTORY_TAGS = ['food', 'weapon', 'armor'] 
# Max number of items that can be found in a room
GROUND_LIMIT = 5
# Text constants
BULLET = '  > '
SEP = ' ● '
# Weapon dict keys
FIST = 'fist'
DAGGER = 'dagger'
SWORD = 'sword'
BOW = 'bow'
# Skill dict keys
FUNCTION = 'function'
DMG = 'dmg'
MESSAGE = 'message'
ISMULTI = 'ismulti'
DOUBLETROUBLE = 'doubletrouble'
ARROWSTORM = 'arrowstorm'
# Rooms/items dict keys
NAME = 'name'
USERDESC = 'userdesc'
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
SHOPINTRO = 'shopintro'
ENEMIES = 'enemies'
DIRECTIONS = [NORTH, SOUTH, EAST, WEST, UP, DOWN]
# Item specific dict keys
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
PICKABLE = 'pickable'
PRICE = 'price'
EDIBLE = 'edible'
WEAPON = 'weapon'
TAG = 'tag' # Tags can be food, weapon, random, decor