from monster import Monster
import cmd


class Combat(cmd.Cmd):
    intro = input('You started a fight, Enemies are staring viciously at you!\n\n')
    prompt_sign = '$'
    prompt = prompt_sign + ' Type <atk> to attack:\n> '
    file = None

    def __init__(self, user, enemies):
        super().__init__()
        self.user = user
        self.enemies = enemies
        self.no_of_enemies = len(enemies)
        self.enemies_dict = self.create_dictionary()

    # Overriding Cmd.emptyline to avoid repitition of last command
    def emptyline(self):
        pass

    # Pre/Post Loop functions
    def preloop(self):
        self.display(False)

    # Creates a dictionary that store Enemies and their corresponding names
    def create_dictionary(self):
        dict = {}
        for i in range(self.no_of_enemies):
            dict[self.enemies[i].name.lower()] = self.enemies[i]
        return dict

    # Returns a string of enemy names
    def list_enemy_names(self):
        names = ''
        for enemy in self.enemies:
            if enemy.alive:
                names += '  - %s\n' % enemy.name
            else:
                pass
        return names

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
    def display(self, clear = True):
        if clear:
            self.clear()
            self.user.show()
            for enemy in self.enemies:
                print(enemy.show())
        else:
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
            choice = input(self.prompt_sign + ' Type <enemy name>:\n' + self.list_enemy_names() + '> ')
            try:
                target_enemy = self.enemies_dict[choice.lower()]
                self.user.attack(target_enemy)
                self.display()
                break
            except KeyError:
                input(self.prompt_sign + " I can't see an enemy with such name!")
                self.display()
        #self.user.attack(enemies_dict[int(arg)])