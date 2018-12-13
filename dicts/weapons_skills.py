'''
Stores weapons and skills
'''
# Imports package namespace which contain all ants
from dicts import *
from player import Player
# Stores weapons usable by player, each weapon is associated with
# a specific skill that synergies with that weapon
WEAPONS = {
#                NAME ----> DMG --> VERB --> SKILL
    FIST   :  {
        NAME: 'Fist',
        DMG:  1,
        VERB: 'punched',
        SKILL: DOUBLETROUBLE,
        },
    DAGGER :  {
        NAME:'Dagger',
        DMG: 2,
        VERB: 'stabbed',
        SKILL: DOUBLETROUBLE,
        },
    SWORD  :  {
        NAME: 'Sword',
        DMG: 3,
        VERB: 'sliced at',
        SKILL: DOUBLETROUBLE,
        },
    BOW    :  {
        NAME: 'Bow',
        DMG: 3,
        VERB: 'fired an arrow at',
        SKILL: ARROWSTORM,
        },
}

# Sets skill dmg according to a dmg multiplier
def set_skills_dmg(init_dmg):
    SKILLS[DOUBLETROUBLE][DMG] = init_dmg * 2
    SKILLS[ARROWSTORM][DMG] = 2

# > Stores skills usable by player all skills have a:
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
            DMG     : None, # x * 2
            ISMULTI : False,
        },
        ARROWSTORM: {
            NAME    : 'Arrow Storm',
            FUNCTION: Player.arrow_storm,
            MESSAGE : 'You fire deadly arrows at all enemies',
            DMG     : None, # 2
            ISMULTI : True,
        },
    }