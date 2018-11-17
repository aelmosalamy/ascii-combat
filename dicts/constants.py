'''
Stores all constants in game, stores window size, tags to be displayed in inventory,
bullets and separators and dict keys.
'''
AC_SCREEN_WIDTH = 80
AC_SCREEN_HEIGHT = 35
# This is the list of tags to be displayed in inventory
INVENTORY_TAGS = ['food', 'weapon', 'armor'] 
# Max number of items that can be found in a room
GROUND_LIMIT = 5
# Text constants
BULLET = '  > '
SEP = ' ● '
# The color used to highlight name with which the user can interact
HIGHLIGHT_COLOR = C.Fore.MAGENTA
# General color constants
CYAN = C.Fore.CYAN
WHITE = C.Fore.WHITE
BRIGHT = C.Style.BRIGHT
DIM = C.Style.NORMAL
# Weapon dict keys
FIST = 'fist'
DAGGER = 'dagger'
SWORD = 'sword'
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
COMBATENEMIES = 'combatenemies'
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