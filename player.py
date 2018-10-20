'''
Manages player, weapons, skills and display
'''
from monster import Monster
import ac_dicts
import colorama as C

class Player(Monster):
    def __init__(self, name, hp, weapon, skill_type=None):
        # weapon[1] is the dmg
        super().__init__(name, hp, weapon[1])
        ac_dicts.net_dmg = self.dmg
        # weapon[0] is name and weapon[2] is hit verb
        self.weapon = weapon[0]
        self.weapon_verb = weapon[2]
        self.enemies = []
        self.skill_type = skill_type
        self.skill = 0
        self.max_skill = 3

    # '●'
    # Displays user stats
    def show(self, size='max'):
        print(C.Fore.MAGENTA + '>', self.name)
        if self.alive:
            print(C.Fore.MAGENTA + '* HP     |' + C.Fore.CYAN + '{}/{}'.format(self.hp, self.max_hp))
        print(C.Fore.MAGENTA + '* Weapon |' + C.Fore.CYAN + '{} (DMG: {})'.format(self.weapon, self.dmg))
        pwr_string = C.Fore.MAGENTA + '* Power  |' + C.Fore.CYAN + ('*' * self.skill) + 'o' * (self.max_skill - self.skill)
        if self.skill == self.max_skill:
            print(pwr_string + ' (Ready!)')
        else: print(pwr_string)

    # Attacks ...
    def attack(self, enemy):
        super().attack(enemy)
        if self.skill < self.max_skill:
            self.skill += 1

    def double_trouble(self, enemy):
        self.attack(enemy)
        self.attack(enemy)
        enemy.update_data()

    # def beam(self, enemy):
    #     enemy.hp = 1
    #     self.skill = 5

    # def shurikens(self, enemies):
    #     for enemy in enemies:
    #         self.attack(enemy)
    #     self.skill = 5
