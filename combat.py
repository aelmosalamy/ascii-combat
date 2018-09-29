from monster import Monster
import cmd


class Combat(cmd.Cmd):
    strings = {
    'intro': 'You started a fight, Enemies are staring viciously at you!',
    'win': 'VICTORY, You defeated all enemies!',
    'syntax_error': 'Oops! I dont understand',
    'unknown_enemy': "I can't see an enemy with such name!",
    'player_attack': "You punched",
    'enemy_death': "died",
    'prompt': 'Type <atk> to attack:',
    }

    intro = input(strings['intro'] + '\n')
    list_symbol = '*'
    prompt_sign = '#'
    prompt = '{}{}\n'.format(prompt_sign, strings['prompt'])

    file = None

    def __init__(self, user, enemies):
        super().__init__()
        self.user = user
        self.user_attack_msg = ''
        self.enemies = enemies
        self.no_of_enemies = len(enemies)
        self.enemies_dict = self.create_dictionary()
        self.enemies_attack_msg = ''

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
                names += '  {} {}\n'.format(self.list_symbol, enemy.name)
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

    # Attacks a chosen enemy
    def user_attack(self, enemy):
        self.user_attack_msg = "{}{} {}".format(self.prompt_sign, self.strings['player_attack'], enemy.name)
        if (enemy.hp - self.user.dmg) <= 0:
            self.user_attack_msg += "\n#{} {}".format(enemy.name, self.strings['enemy_death'])
        self.user.attack(enemy)
    
    # All alive enemies attacks the user returning a hit string
    def enemies_attack(self):
        messages = ''
        for enemy in self.enemies:
            if enemy.alive:
                enemy.attack(self.user)
                hit_string = "!! {} {} you. ({}HP)\n".format(enemy.name, enemy.action, str(-enemy.dmg))
                messages += hit_string
        self.enemies_attack_msg = messages
        
    # Displays the interface: All Enemies and user status
    def display(self, clear = True):
        if clear:
            self.clear()
        self.user.show()
        for enemy in self.enemies:
            print(enemy.show())
        print(self.user_attack_msg) 
        print(self.enemies_attack_msg)
         
    # Clears the terminal by adding new lines
    def clear(self, no_of_lines = 40):
        print('\n' * no_of_lines)

    # Cmd commands
    def do_atk(self, arg):
        """Attacks a specific enemy: atk <enemy name>"""
        self.display()
        while True:
            choice = input(self.prompt_sign + 'Type <enemy name>:\n' + self.alive_enemy_names() + '> ')
            self.enemies_dict = self.create_dictionary()
            try:
                target_enemy = self.enemies_dict[choice.lower()]
                self.user_attack(target_enemy)
                self.enemies_attack()
                self.display()
                return True
            except KeyError:
                input(self.prompt_sign + self.strings['unknown_enemy'])
                self.display()
