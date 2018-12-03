'''
This is just "main" module that launchs our game
and start the cmdloop()
'''
from dicts.weapons_skills import *
from dicts.rooms import *
from dicts.utils import *
from dicts.monsters import give_monster
import combat, dungeon, sys

def main():
    sys.path.append(os.getcwd())
    set_console_size()
    me = Player('Bori', 10, WEAPONS[DAGGER], SKILLS[ARROWSTORM])
    enemies = [give_monster('wolf') for i in range(3)]

    # Comment/Uncomment game/world depending on which one you want to try
    # world is the dungeon system, game is the combat system, they are not
    # joined together yet, untill then this what you can do
    world = dungeon.Dungeon(me, ROOMS)
    world.cmdloop()
    # game = combat.Combat(me, enemies)
    # game.cmdloop()

if __name__ == '__main__':
    main()  

