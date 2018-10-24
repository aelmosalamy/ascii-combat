'''
This contains multiple dictionaries of different enemies, weapons, and so on
'''
from monster import Monster
from player import Player
from random import choice

# Damage to be used for skills usually equals to player's current dmg
initial_dmg = 0

# DATA DICTIONARIES
MONSTER_VARIATION = ['Ruthless', 'Ferocious', 'Demonic',
                     'Brutal', 'Bloody', 'Violent', 'Wild', 'Spooky',
                     'Murderous', 'Fierce', 'Savage', 'Monsterous', 
                     'Hideous', 'Grotesque',
                    ]

'''Stores specie names and its equivalent stats
in a dictionary, 2 word names must be separated
with a "dash (-)"
'''
MONSTER_SPECIES = {
    #Specie         |  NAME  | HP |  DMG  |  ACTION |
    'chicken':      ['Chicken', 1, 1,      'pinched'],
    'archer':       ['Archer', 1, 2,          'shot'],
    'spider':       ['Spider', 2, 1,           'hit'],
    'scorpion':     ['Scorpion', 1, 3,       'stung'],
    'guard':        ['Guard', 2, 2,        'punched'],
    'wolf':         ['Wolf', 3, 1,            'bit'],
    'werewolf':     ['Werewolf', 3, 2,        'bit'],
    'alligator':    ['Alligator', 3, 3,       'bit'],
    'bear':         ['Bear', 4, 2,      'slashed at'],
    'ogre':         ['Ogre', 5, 3,         'slammed'],
    'pbag':         ['Punching-Bag', 10, 0,       ''],
    'spbag':        ['Super-Punching-Bag', 999, 0,''],
}

'''
Stores of weapons and their equivalent dmg, weapon names
start with a capital letter
'''
WEAPONS = {
#                NAME ----> DMG --> VERB
    'fist'   :  ['Fist',   1,   'punched'],
    'dagger' :  ['Dagger', 2,   'stabbed'],
    'sword'  :  ['Sword',  3, 'sliced at'],
}

'''
Stores player skills
'''
SKILLS = {    
        'DOUBLE_TROUBLE': {
            'name'    : 'Double Trouble',
            'function': Player.double_trouble,
            'message' : 'twice in quick succession',
            'dmg'     : None,
            'ismulti' : False,
        },
        'ARROW_STORM': {
            'name'    : 'Arrow Storm',
            'function': Player.arrow_storm,
            'message' : 'You throw deadly arrows on all enemies',
            'dmg'     : 2,
            'ismulti' : True,
        },
    }

def set_skills_dmg():
    SKILLS['DOUBLE_TROUBLE']['dmg'] = initial_dmg * 2
    SKILLS['ARROW_STORM']['dmg'] = 2
    


# EXTRACTOR FUNCTIONS
def give_monster(specie, use_special_name=False):
    mySpecieStats = MONSTER_SPECIES[specie]
    x = Monster(mySpecieStats[0], mySpecieStats[1], mySpecieStats[2], mySpecieStats[3])
    if use_special_name:
        # Generating a name using MONSTER_VARIATION
        adjective = choice(MONSTER_VARIATION)
        MONSTER_VARIATION.remove(adjective)
        x.name = '{} {}'.format(adjective,  x.name)
    return x

