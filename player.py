'''
A Player class, every player got: HP, DMG, WEAPON and a SKILL
'''
import colorama as C

from dicts import weapons_skills as ws
from dicts.weapons_skills import *
from monster import Monster


class Player(Monster):
    def __init__(self, name, hp, weapon):
        super().__init__(name, hp, weapon[DMG])
        # Sets skills dmg
        ws.set_skills_dmg(self.dmg)
        self.weapon = weapon
        self.weapon_verb = self.weapon[VERB]
        self.enemies = []
        self.skill_type = ws.SKILLS[weapon[SKILL]]
        self.skill = 0
        self.max_skill = 3

    # Displays user stats
    def show(self, size='max'):
        print(C.Fore.MAGENTA + '>', self.name)
        if self.alive:
            print(C.Fore.MAGENTA + '* HP     |' + C.Fore.CYAN + '█' * self.hp + '░' * (self.max_hp - self.hp) + ' ' + str(self.hp))
        print(C.Fore.MAGENTA + '* Weapon |' + C.Fore.CYAN + '{} (DMG: {})'.format(self.weapon[NAME], self.dmg))
        print(C.Fore.MAGENTA + '* Skill  |' + C.Fore.CYAN + '{}'.format(self.skill_type['name']))
        pwr_string = C.Fore.MAGENTA + '* Power  |' + C.Fore.CYAN + ('*' * self.skill) + 'o' * (self.max_skill - self.skill)
        if self.skill == self.max_skill:
            print(pwr_string + ' (Ready!)')
        else:
            print(pwr_string)

    # Attacks ...
    def attack(self, enemy):
        super().attack(enemy)
        if self.skill < self.max_skill:
            self.skill += 1
    
    # Skill functions
    def double_trouble(self, enemy):
        enemy.hp -= ws.SKILLS[DOUBLETROUBLE]['dmg']
        enemy.update_data()

    def arrow_storm(self, enemies):
        for enemy in enemies:
            enemy.hp -= ws.SKILLS[ARROWSTORM]['dmg']
            enemy.update_data()
