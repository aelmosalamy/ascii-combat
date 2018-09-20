from player import Player
from combat import *


def main():
    me = Player('My Player', 10, 2)
    enemies = []
    for i in range(3):
        mon = Monster('Spider %s' % i, 2, 1)
        enemies.append(mon)

    game = Combat(me, enemies)
    game.cmdloop()


if __name__ == '__main__':
    main()
