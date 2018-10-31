'''
Instantiate this to create a Combat 'scene' containing a player and enemies
both must be given, run the Combat.cmdloop() to start the scene
'''
from monster import Monster
from ac_dicts import *
import colorama as C
import cmd, platform, os

class Combat(cmd.Cmd):
    STRINGS = {
    'intro'        : 'You started a fight, Enemies are staring viciously at you!\nPress Enter to start . . .',
    'win'          : 'VICTORY, You defeated all enemies!\nPress Enter to Exit . . .',
    'lose'         : 'DEFEAT, You got beaten by enemies!\nPress Enter to Exit . . .',
    'syntax_error' : 'Oops! I dont understand',
    'unknown_enemy': "I can't see that enemy!",
    'enemy_death'  : "You eliminated",
    'user_death'   : "You are bleeding too much.. Argh!",
    'full_hp'      : "You are perfectly healthy!",
    'prompt'       : 'Type <atk> to attack:\n> ',
    'prompt_skl'   : 'Type <atk> or <skl>:\n> ',
    'atk_choice'   : 'Attack .. Choose enemy number:\n',
    'skl_choice'   : 'Skill  .. Choose enemy number:\n',
    'no_skl'       : "Oops! It seems like you haven't acquired a skill yet!",
    'no_pwr'       : 'Argh! not enough power to use your skill!',
    }

    # Global constants
    LIST_SYMBOL = '  *'
    PROMPT_SIGN = '# '


    def __init__(self, user, enemies):
        # cmd.Cmd initialization
        super().__init__()
        # Color settings
        if platform.system() == 'Windows':
            C.init()
        print(C.Fore.WHITE + C.Back.BLACK + C.Style.BRIGHT, end='')
        self.intro = input(self.STRINGS['intro'])
        self.prompt = '{}{}'.format(self.PROMPT_SIGN, self.STRINGS['prompt'])
        # user/enemies variables
        self.user = user
        self.STRINGS['player_attack'] = 'You ' + self.user.weapon_verb
        self.user_attack_msg = ''
        self.enemies = enemies
        self.no_of_enemies = len(enemies)
        self.enemies_dict = self.create_dictionary()
        self.enemies_attack_msg = ''

    # cmd.Cmd method overriding
    # Avoids repitition of last command
    def emptyline(self):
        self.display()
        pass

    # Error message for unknown commands
    def default(self, line):
        self.display()
        print(C.Back.RED + C.Fore.RED + '{}{} <{}>{}'.format(self.PROMPT_SIGN, self.STRINGS['syntax_error'], line, C.Back.BLACK))
        print(C.Back.BLACK + C.Fore.WHITE, end='')
    
    # Removes the help method
    def do_help(self, arg):
        self.display()
        pass

    # Controls termination of Combat, win/lose msg
    def postcmd(self, stop, line):
        # Checks win condition
        if not self.enemies_alive():
            print(C.Back.GREEN + C.Fore.GREEN + self.PROMPT_SIGN + self.STRINGS['win'] + C.Back.BLACK, end='')
            input()
            return True
        elif self.enemies_alive() and not self.user.alive:
            print(C.Back.RED + C.Fore.RED + self.PROMPT_SIGN + self.STRINGS['lose'] + C.Back.BLACK, end='')
            input()
            return True
        # Changes prompt if Skill is available to use
        if self.user.skill == self.user.max_skill:
            self.prompt = self.PROMPT_SIGN + self.STRINGS['prompt_skl']
        else: 
            self.prompt = self.PROMPT_SIGN + self.STRINGS['prompt']

    # Pre/Post Loop functions
    def preloop(self):
        self.display()

    # ENEMIES, PLAYER, COMBAT STUFF
    # Creates a dictionary that store Enemies and their corresponding names
    def create_dictionary(self):
        dict = {}
        counter = 1
        for enemy in self.enemies:
            if enemy.alive:
                dict[str(counter)] = enemy
                counter += 1
        return dict

    # Returns a string of alive enemy names
    def alive_enemy_names(self):
        names = ''
        counter = 1
        for enemy in self.enemies:
            if enemy.alive:
                names += '  {}| {}\n'.format(counter, enemy.name)
                counter += 1
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

    # Checks if enemy will die from a specific blow and returns a string accordingly
    def enemy_death_msg(self, enemy, dmg_taken):
        if (enemy.hp - dmg_taken) <= 0:
            # Message if enemy is dead
            outcome = "\n{}{}{} {}{}".format(C.Style.BRIGHT + C.Back.RED + C.Fore.RED, 
            self.PROMPT_SIGN, self.STRINGS['enemy_death'], enemy.name, C.Back.BLACK)
        else:
            outcome = ''
        return outcome

    # Attacks a chosen enemy
    def user_attack(self, enemy):
        self.user_attack_msg = "{}{}{} {} (-{}HP)".format(C.Style.BRIGHT + C.Back.BLACK + C.Fore.CYAN, self.PROMPT_SIGN,
        self.STRINGS['player_attack'], enemy.name, self.user.dmg)
        self.user_attack_msg += self.enemy_death_msg(enemy, self.user.dmg)
        self.user.attack(enemy)

    # Attacks enemy using the player's current skill
    def user_skill(self, enemies):
        my_skill = self.user.skill_type
        # Executes skill depending multi-target/single-target skill
        if my_skill['ismulti']:
            self.user_attack_msg = (C.Style.BRIGHT + C.Back.BLACK + C.Fore.MAGENTA +
            "{}SKILL: {} >>>\n{} (-{}HP to all)".format(self.PROMPT_SIGN, my_skill['name'].upper(),
            my_skill['message'], my_skill['dmg']))
            for enemy in enemies:
                self.user_attack_msg += self.enemy_death_msg(enemy, my_skill['dmg'])
            my_skill['function'](self.user, enemies)
        else:
            self.user_attack_msg = (C.Style.BRIGHT + C.Back.BLACK + C.Fore.MAGENTA +
            "{}SKILL: {} >>>\n{} {} {} (-{}HP)".format(self.PROMPT_SIGN, my_skill['name'].upper(), self.STRINGS['player_attack'],
            enemies.name, my_skill['message'], my_skill['dmg']))
            self.user_attack_msg += self.enemy_death_msg(enemies, my_skill['dmg'])
            my_skill['function'](self.user, enemies)
        self.user.skill = 0

    # All alive enemies attacks the user and returns a hit string
    def enemies_attack(self):
        messages = C.Style.BRIGHT + C.Back.BLACK + C.Fore.RED
        for enemy in self.enemies:
            if enemy.alive:
                if enemy.dmg == 0:
                    hit_string = ''
                else:
                    enemy.attack(self.user)
                    hit_string = "!! {} {} you (-{}HP)\n".format(enemy.name, enemy.action, str(enemy.dmg))
                messages += hit_string
        messages += C.Style.BRIGHT + C.Back.CYAN + C.Fore.CYAN
        if self.user.hp <= 0:
            messages += self.PROMPT_SIGN + self.STRINGS['user_death'] + C.Back.BLACK
        elif self.user.hp == self.user.max_hp:
            messages += self.PROMPT_SIGN + self.STRINGS['full_hp'] + C.Back.BLACK
        else:
            messages += '{}You survived enemy attacks with {}/{} HP left{}'.format(self.PROMPT_SIGN, self.user.hp, self.user.max_hp, C.Back.BLACK)
        self.enemies_attack_msg = messages

    # UTILITY FUNCTIONS   
    # Displays the interface: All Enemies and user status
    def display(self, clear = True):
        if clear:
            self.clear()
        print(C.Style.BRIGHT + C.Back.BLACK + C.Fore.WHITE)
        self.user.show()
        for enemy in self.enemies:
            if enemy.alive:
                print(C.Style.BRIGHT + C.Back.BLACK + C.Fore.RED + enemy.show())
            else:
                print(C.Style.DIM + C.Back.BLACK + C.Fore.RED + enemy.show())
        print(self.user_attack_msg) 
        print(self.enemies_attack_msg)
        print(C.Style.BRIGHT + C.Back.BLACK + C.Fore.WHITE)
         
    # Clears the terminal using the approperiate subshell command
    # for each terminal
    @staticmethod
    def clear():
        print(C.Style.BRIGHT + C.Back.BLACK + C.Fore.WHITE, end='')
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')
    
    # A wrapper for printing a RED error message
    def error_msg(self, text):
        self.display()
        print(C.Back.RED + C.Fore.RED + 
        self.PROMPT_SIGN + text +
        C.Back.BLACK + C.Fore.WHITE)

    # A loop that executes any given function on an enemy
    # whenever a valid input is entered
    def demand_and_execute(self, function, _prompt=STRINGS['atk_choice']):
        self.display()
        while True:
            choice = input(self.PROMPT_SIGN + _prompt + self.alive_enemy_names() + '> ')
            self.enemies_dict = self.create_dictionary()
            try:
                target_enemy = self.enemies_dict[choice.lower()]
                function(target_enemy)
                self.enemies_attack()
                self.display()
                return True
            except KeyError:
                print(C.Back.RED + C.Fore.RED, end='')
                input(self.PROMPT_SIGN + self.STRINGS['unknown_enemy'])
                self.display()
                    
    # USER INPUT AND COMMANDS
    # Cmd commands
    def do_atk(self, arg):
        """Attacks a specific enemy, type <atk>"""
        self.demand_and_execute(self.user_attack)

    def do_skl(self, arg):
        """Unleashs special power using up all power points, type <skl>"""
        if self.user.skill_type == None:
            self.error_msg(self.STRINGS['no_skl'])
        elif self.user.skill == self.user.max_skill:
            # Multi and single target skill execution
            if not self.user.skill_type['ismulti']:
                self.demand_and_execute(self.user_skill, self.STRINGS['skl_choice'])
            else:
                enemies_list = []
                for enemy in self.enemies:
                    if enemy.alive:
                        enemies_list.append(enemy)
                self.user_skill(enemies_list)
                self.enemies_attack()
                self.display()
        else:
            self.error_msg(self.STRINGS['no_pwr'])
