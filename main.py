from player import Player
import combat
from ac_dicts import *
import os, platform

# Configuring CMD's window
if platform.system() == 'Windows':
    os.system('title ASCII Combat')
    os.system('mode con: cols=70 lines=30')
elif platform.system() == 'Linux' or 'Darwin':
    os.system('echo -n -e "\033]0;ASCII Combat\007"')
    os.system('resize -s 30 60')

def main():
    me = Player('My Player', 10, 2)
    enemies = []
    for i in range(1):
        m = give_monster('wolf')
        enemies.append(m)
    enemies.append(give_monster('scorpion'))
    enemies.append(give_monster('bear'))

    game = combat.Combat(me, enemies)
    game.cmdloop()


if __name__ == '__main__':
    main()  

