from monster import Monster
import cmd


class Combat(cmd.Cmd):
    intro = input('You started a fight, Enemies are staring viciously at you!')
    prompt = 'Type: <atk> to attack enemy.\n> '
    file = None

    def __init__(self, user, enemies):
        super().__init__()
        self.user = user
        self.enemies = enemies
        self.no_of_enemies = len(enemies)

    # Pre/Post Loop functions
    def preloop(self):
        self.display()
    # Creates a dictionary with storing Enemies and their corresponding names
    # for comparing to user inputs
    def create_dictionary(self):
        dict = {}
        for i in range(self.no_of_enemies):
            dict[i] = self.enemies[i]
            return dict

    # Checks if all enemies are alive
    def enemies_alive(self):
        for enemy in self.enemies:
            if not enemy.alive:
                self.no_of_enemies -= 1
        if self.no_of_enemies > 0:
            return True
        else:
            return False

    # All alive enemies attacks the user
    def enemies_attack(self):
        for enemy in enemies:
            enemy.attack(self.user)

    # Displays the interface: All Enemies and user status
    def display(self):
        self.user.show()
        for enemy in self.enemies:
            print(enemy.show())

    # Attacks a chosen enemy
    def do_atk(self, arg):
        """Attacks a specific enemy: atk <enemy name>"""

        enemies_dict = self.create_dictionary()
        #self.user.attack(enemies_dict[int(arg)])
        self.display()

# x = Combat(3, [5, 5])
# x.cmdloop()

##    exitGame = False
##    case = 0
##    msg = ''
##    xmsg = ''
##    hit_msg = ''
##    enemies = []
##    no_of_enemies = 3
##    for enemy in range(no_of_enemies):
##        x = Monster('Giant Spider ' + str(enemy + 1), 3, 1, 'You got hit by a sticky web')
##        enemies.append(x)
##
##    player_name = input('Enter your name: ')
##    me = Player(player_name, 10, 2)
##
##    # Main loop
##    while exitGame == False:
##        print('\n' * 120)
##        for enemy in enemies:
##            enemy.show('min')
##        me.show()
##        # Print comment
##        print('_' * 20)
##        print(msg)
##        print(hit_msg)
##        print(xmsg+'\n\n')
##        # End Conditions
##        # Win
##        if case == 4:
##            exitGame = True
##            continue
##        # Lose
##        elif case == 5:
##            exitGame = True
##            continue
##        if me.special_power == 0:
##            i = input('Type ATK or PWR ... ')
##        else:
##            i = input('Type ATK ... ')
##
##        # Reads inputs, case 0 = none, 1 = atk, 2 = ray, 3 = bmb, 4 = won
##        if i.lower() == 'atk':
##            i = input('*ATK* Which Enemy? (from 1 to ' + str(no_of_enemies) + ') ')
##            me.attack(enemies[int(i) - 1])
##            if enemies[int(i)-1].alive:
##                case = 1
##            else:
##                case = 6
##        elif i.lower() == 'pwr':
##            i = input('*PWR* Death-Ray or Mega-Bomb-01.. Type RAY or BMB ... ')
##            if i.lower() == 'ray':
##                i = input('*RAY* Which Enemy? (from 1 to ' + str(no_of_enemies) + ') ')
##                me.super_ray(enemies[int(i) - 1])
##                case = 2
##            elif i.lower() == 'bmb':
##                me.attack_all(enemies)
##                case = 3
##        hit_msg = ''
##        for enemy in enemies:
##            if enemy.alive:
##                enemy.attack(me)
##                hit_msg += (enemy.atk_msg + '\n')
##                if me.hp <= 0:
##                    case = 5
##                    me.generate_quote()
##
##
##        # Messages
##        if case == 0:
##            msg = ''
##        elif case == 1:
##            msg = '*ATK* You hit the ' + enemies[int(i) - 1].name + ' (-2)'
##        elif case == 2:
##            msg = '*RAY* You burned the ' + enemies[int(i) - 1].name + ' to 1 HP.'
##        elif case == 3:
##            msg = '*BMB* You ZaPpEd all enemies (-2)'
##        elif case == 5:
##            msg = 'You got beaten by the monsters :c'
##        elif case == 6:
##            msg = 'You crushed the ' + enemies[int(i)-1].name
##
##        # Checks if enemies are dead
##        j = no_of_enemies
##        for enemy in enemies:
##            if not enemy.alive:
##                j -= 1
##            if j <= 0:
##                case = 4
##        if case == 4:
##            xmsg = 'You CRUSHED all of your opponents'
##
##    input('Press Enter to exit ...')
