'''
Stores weapons and skills
'''
# Imports package namespace which contain all constants
from dicts import *
from player import Player
# Stores weapons usable by player, all weapons got a:
# Weapon[0] is the weapon name, Weapon[1] is the weapon dmg
# Weapon[2] is the verb written when atk is used
WEAPONS = {
#                NAME ----> DMG --> VERB
    FIST   :  ['Fist',   1,   'punched'],
    DAGGER :  ['Dagger', 2,   'stabbed'],
    SWORD  :  ['Sword',  3, 'sliced at'],
}

# Sets skill dmg according to a dmg multiplier
def set_skills_dmg(init_dmg):
    SKILLS[DOUBLETROUBLE][DMG] = init_dmg * 2
    SKILLS[ARROWSTORM][DMG] = 2

# > Stores skills usable by player all skills got a:
# - NAME (Just a name)
# - FUNCTION (The skill function declared in the Player.class)
# - MESSAGE (Text displayed when skill is used)
# - DMG (Damage dealt by that skill)
# - ISMULTI (True if multi-target skill)
# Note: SKILLS DMG IS ASSIGNED AT RUNTIME SINCE IT SCALES WITH PLAYER'S DMG
SKILLS = {
        'NONE': {
            NAME    : 'None',
        },
        DOUBLETROUBLE: {
            NAME    : 'Double Trouble',
            FUNCTION: Player.double_trouble,
            MESSAGE : 'twice in quick succession',
            DMG     : None,
            ISMULTI : False,
        },
        ARROWSTORM: {
            NAME    : 'Arrow Storm',
            FUNCTION: Player.arrow_storm,
            MESSAGE : 'You throw deadly arrows on all enemies',
            DMG     : None,
            ISMULTI : True,
        },
    }
