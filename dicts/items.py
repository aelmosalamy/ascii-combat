'''
Stores all items in game, an item is anything you can pick, store in inventory or look at
and sometimes, eat.

> Must-have item attributes:
NAME, GROUNDDESC, SHORTDESC, LONGDESC, PICKABLE, EDIBLE, TAG

> Optional item attributes:
PRICE (If sold in a shop), WEAPON (If used as weapon)
'''

# Imports package namespace which contain all constants
from dicts import *
from dicts.weapons_skills import WEAPONS

# Returns a list of the names of items with a specific tag assigned to them
def get_tag_items(item_names, tag):
    return [x for x in item_names if ITEMS[x][TAG] == tag]

# Returns items GROUNDDESC as bullet points
def get_items_grounddesc(room, item_look=None):
    text = ''
    for item_name in room[GROUND]:
        item = ITEMS[item_name]
        # Add item GROUNDDESC to be displayed
        text += '{} {} {}'.format(BULLET + item[GROUNDDESC][0],
        HIGHLIGHT_COLOR + item[NAME].lower() + WHITE,
        item[GROUNDDESC][1] + '\n')
    return text

# Returns items SHORTDESC as bullet points
def get_items_shortdesc(item_names):
    text = ''
    for item_name in item_names:
        item = ITEMS[item_name]
        # Add item SHORTDESC to be displayed
        text += BULLET + item[SHORTDESC] + '\n'
    return text

# coin items and their prices (Must use the exact name as their counterpart in ITEMS)
# A sack contains 10x items, its value depends on the contained item's value
COIN_VALUE = {
    'coin': 1,
    'gold coin': 7,
    'coins sack': 10,
    'gold coins sack': 70,
}

# GROUNDDESC is split into two, because later the item will be
# colored and insered between them
ITEMS = {
    'apple': {
        NAME: 'Apple',
        GROUNDDESC: ['An', 'lies in the dirt'],
        SHORTDESC: 'a red, shiny apple',
        LONGDESC: 'This is a delicious, edible fruit. Perhaps you can eat it.',
        PICKABLE: True,
        EDIBLE: True,
        TAG: 'food',
    },
    'cake': {
        NAME: 'Cake',
        GROUNDDESC: ['A lovely vanilla', 'is inside a box placed on ground'],
        SHORTDESC: 'a tasty vanilla cake',
        LONGDESC: 'This delicious treat was baked with love at the Grand Bakery, made from authentic vanilla and chocochips',
        PICKABLE: True,
        PRICE: 10,
        EDIBLE: True,
        TAG: 'food',
    },
    'bread': {
        NAME: 'Bread',
        GROUNDDESC: ['A loaf of', 'lies on ground'],
        SHORTDESC: 'a warm loaf of bread',
        LONGDESC: 'A tasty bread loaf, baked until it puffed up, and became soft and crunchy',
        PICKABLE: True,
        PRICE: 3,
        EDIBLE: True,
        TAG: 'food',
    },
    'flatbread': {
        NAME: 'Flatbread',
        GROUNDDESC: ['A piece of', 'lies on ground'],
        SHORTDESC: 'a plain flatbread',
        LONGDESC: 'Flatbread is made with flour, water and salt, before it is rolled into flattened dough',
        PICKABLE: True,
        PRICE: 1,
        EDIBLE: True,
        TAG: 'food',
    },
    'beef': {
        NAME: 'Beef',
        GROUNDDESC: ['A cut of', 'is thrown on ground'],
        SHORTDESC: 'a cut of beef',
        LONGDESC: 'A raw piece of meat, brought from the southern meadows, it is tastier when cooked!',
        PICKABLE: True,
        PRICE: 35,
        EDIBLE: True,
        TAG: 'food',
    },
    'sausage': {
        NAME: 'Sausage',
        GROUNDDESC: ['A fresh', 'lies on the floor'],
        SHORTDESC: 'a fresh sausage',
        LONGDESC: 'A cylindrical piece of meat, delicious and perfect for BBQ!',
        PICKABLE: True,
        PRICE: 20,
        EDIBLE: True,
        TAG: 'food',
    },
    'fountain': {
        NAME: 'Fountain',
        GROUNDDESC: ['A white', 'is streaming water'],
        SHORTDESC: 'a fabulous, marble fountain',
        LONGDESC: 'This beautiful sculpture is emanating water, attracting various kinds of birds.',
        PICKABLE: False,
        EDIBLE: False,
        TAG: 'decor',
    },
    'evergreen': {
        NAME: 'Evergreen',
        GROUNDDESC: ['A vibrant', 'confidently rises from the earth'],
        SHORTDESC: 'a fragrant evergreen, complete with bristles',
        LONGDESC: 'Deep green bristles erupt in a spire around this proud tree, fixed firmly in the ground.',
        PICKABLE: False,
        EDIBLE: False,
        TAG: 'decor',
    },
    'dagger': {
        NAME: 'Dagger',
        GROUNDDESC: ['A rusty', 'is thrown on the ground'],
        SHORTDESC: 'a rusty, old dagger',
        LONGDESC: 'This dagger, ancient and rusty as it is, is still sharp enough to be used as a weapon.',
        PICKABLE: True,
        EDIBLE: False,
        WEAPON: WEAPONS[DAGGER],
        TAG: 'weapon',
    },
    'sword': {
        NAME: 'Sword',
        GROUNDDESC: ['A long', 'is thrown on the ground'],
        SHORTDESC: 'a long, iron sword',
        LONGDESC: 'This sword is ancient. despite being forged from iron, it will slice through your enemies with ease, ',
        PICKABLE: True,
        EDIBLE: False,
        WEAPON: WEAPONS[SWORD],
        TAG: 'weapon',
    },
    'coin': {
        NAME: 'Coin',
        GROUNDDESC: ['A bronze', 'is dropped on the ground'],
        SHORTDESC: 'a bronze coin',
        LONGDESC: "This is a bronze coin, You can spend it at any shop in exchange for useful goods",
        PICKABLE: True,
        EDIBLE: False,
        TAG: 'coins',
    },
}