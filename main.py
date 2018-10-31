from ac_dicts import *
import player
import combat
import dungeon
import os, platform

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 30

# Configuring CMD's window
if platform.system() == 'Windows':
    os.system('title ASCII Combat')
    os.system('mode con: cols={} lines={}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
elif platform.system() == 'Linux' or platform.system() == 'Darwin':
    os.system('echo -n -e "\033]0;ASCII Combat\007"')
    os.system('resize -s {} {}'.format(SCREEN_HEIGHT, SCREEN_WIDTH))

def main():
    me = player.Player('Bori', 10, WEAPONS[DAGGER], SKILLS['DOUBLE_TROUBLE'])
    enemies = [give_monster('wolf') for i in range(3)]
    # world = dungeon.Dungeon(me, ROOMS)
    # world.cmdloop()
    game = combat.Combat(me, enemies)
    game.cmdloop()

if __name__ == '__main__':
    main()  

