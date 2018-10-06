from player import Player
import combat


def main():
    me = Player('My Player', 10, 2)
    enemies = []
    for i in range(2):
        m = combat.Monster('Spider %s' % (i+1), 2, 1)
        enemies.append(m)

    game = combat.Combat(me, enemies)
    game.cmdloop()


if __name__ == '__main__':
    main()

    