'''
This contains multiple dictionaries of different enemies, weapons, and so on
'''
from monster import Monster
from random import choice

# DATA DICTIONARIES
'''
 Monster = specie : 
           name   : ___
           hp     : ___
           dmg    : ___
           action : ___
'''
MONSTER_VARIATION = ['Fiery', 'Ruthless', 'Ferocious',
                     'Brutal', 'Bloody', 'Creepy', 'Violent', 'Wild', 'Spooky',
                     'Murderous', 'Fierce', 'Savage', 'Monsterous', 'Hideous',
                     'Horrid', 'Grotesque',
                    ]

'''Stores specie names and its equivalent stats
in a dictionary'''
MONSTER_SPECIES = {
    #Specie         |  NAME | HP | DMG | ACTION |
    'spider':       ['Spider', 2, 1, 'hit' ],
    'wolf':         ['Wolf', 3, 1,   'bite'],
    'bear':         ['Brown Bear', 4, 2, 'slashed at'],
    'scorpion':     ['Scorpion', 1, 2, 'stinged'],
}


# GENERATOR FUNCTIONS
def generate_monsters():
    pass

# EXTRACTOR FUNCTIONS

def give_monster(specie, use_specie_name=False):
    mySpecie = MONSTER_SPECIES[specie]
    x = Monster(mySpecie[0], mySpecie[1], mySpecie[2], mySpecie[3])
    if not use_specie_name:
        # Generating a name using MONSTER_VARIATION
        y = choice(MONSTER_VARIATION)
        MONSTER_VARIATION.remove(y)
        x.name = '{} {}'.format(y,  x.name)
    return x

