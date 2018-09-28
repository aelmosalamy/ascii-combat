from monster import Monster
import cmd


class Combat(cmd.Cmd):
    intro = input('You started a fight, Enemies are staring viciously at you!\n\n')
    prompt_sign = '#'
    prompt = prompt_sign + 'Type <atk> to attack:\n> '
    strings = {
        'win': 'VICTORY, You demolished all enemies!',
        'syntax_error': 'Oops! I dont understand',
        'unknown_enemy': "I can't see an enemy with such name!"
    }
    file = None

    def __init__(self, user, enemies):
        super().__init__()
        self.user = user
        self.enemies = enemies
        self.no_of_enemies = len(enemies)
        self.enemies_dict = self.create_dictionary()

    # cmd.Cmd method overriding
    # Avoids repitition of last command
    def emptyline(self):
        pass

    # Error message for unknown commands
    def default(self, line):
        print('{}{} <{}>'.format(self.prompt_sign, self.strings['syntax_error'], line))

    # Controls termination of Combat
    def postcmd(self, stop, line):
        if not self.enemies_alive():
            input(self.prompt_sign + self.strings['win'])
            return True

    # Pre/Post Loop functions
    def preloop(self):
        self.display(False)

    # Creates a dictionary that store Enemies and their corresponding names
    def create_dictionary(self):
        dict = {}
        for enemy in self.enemies:
            if enemy.alive:
                dict[enemy.name.lower()] = enemy
        return dict

    # Returns a string of alive enemy names
    def alive_enemy_names(self):
        names = ''
        for enemy in self.enemies:
            if enemy.alive:
                names += '  + {}\n'.format(enemy.name)
            else:
                pass
        return names

    # Are any enemy alive? True/False
    def enemies_alive(self):
        self.no_of_enemies = len(self.enemies)
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
    def display(self, clear = True):
        if clear:
            self.clear()
        self.user.show()
        for enemy in self.enemies:
            print(enemy.show())     

    # Clears the terminal by adding new lines
    def clear(self, no_of_lines = 40):
        print('\n' * no_of_lines)

    # Attacks a chosen enemy
    def do_atk(self, arg):
        """Attacks a specific enemy: atk <enemy name>"""
        self.display()
        while True:
            choice = input(self.prompt_sign + 'Type <enemy name>:\n' + self.alive_enemy_names() + '> ')
            self.enemies_dict = self.create_dictionary()
            try:
                target_enemy = self.enemies_dict[choice.lower()]
                self.user.attack(target_enemy)
                self.display()
                return True
            except KeyError:
                input(self.prompt_sign + self.strings['unknown_enemy'])
                self.display()
