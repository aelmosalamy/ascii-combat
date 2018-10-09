from monster import Monster

class Player(Monster):
    def __init__(self, name, hp, dmg):
        super().__init__(name, hp, dmg)
        self.enemies = []
        self.max_power = 3
        self.special_power = 3

    # '●'
    # Displays user stats
    def show(self, size='max'):
        print('>', self.name)
        if self.alive:
            print('* HP:', '#' * self.hp)
        print('* DMG:', self.dmg)
        print('* POWER:', '*' * (self.max_power - self.special_power) + 'o' * self.special_power)

    # Attacks ...
    def attack(self, enemy):
        super().attack(enemy)
        if self.special_power > 0:
            self.special_power -= 1

    def super_ray(self, enemy):
        enemy.hp = 1
        self.special_power = 5

    def attack_all(self, enemies):
        for enemy in enemies:
            self.attack(enemy)
        self.special_power = 5
