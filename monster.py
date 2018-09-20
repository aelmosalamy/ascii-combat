class Monster:
    def __init__(self, name, hp, dmg, atk_msg='You got hit'):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.dmg = dmg
        self.alive = True
        self.atk_msg = atk_msg + ' (-' + str(self.dmg) + ')'
        self.length = 0

    def line(self, shape):
        if shape == 'top':
            return '┌' + '-' * self.length + '┐'
        elif shape == 'mid':
            return '---' * self.length
        elif shape == 'bot':
            return '└' + '-' * self.length + '┘'
        elif shape == 'clear':
            return '\n' * 120

    def attack(self, enemy):
        enemy.hp -= self.dmg

    # Returns a multi-line string of the stats
    def show(self, size='min'):
        total = ''
        self.update_data()
        if size == 'max':
            if self.alive:
                n = '|' + self.name
                total += self.line('top') + '\n'
                total += n + ((self.length - len(n)) * ' ') + ' |\n'
                n = '|'+'HP:'+'#' * self.hp
                total += n + ((self.length - len(n)) * ' ') + ' |\n'
                n = '|'+'DMG:'+ str(self.dmg)
                total += n + ((self.length - len(n)) * ' ') + ' |'
                total += '\n' + self.line('bot')
                return total
            else:
                total = ''
                n = '|' + self.name
                total += self.line('top') + '\n'
                total += n + ((self.length - len(n)) * ' ') + ' |'
                total += '\n' + self.line('bot')
                return total
        elif size == 'min':
            if self.alive:
                n = '|' + self.name + ' |HP: ' + '#' * self.hp + ' |DMG: ' + str(self.dmg)
                self.length = len(n)
                total += self.line('top') + '\n'
                total += n +((self.length - len(n)) * ' ') + ' |'
                total += '\n' + self.line('bot')
                return total
            else:
                n = '|' + self.name
                self.length = len(n)
                total += self.line('top') + '\n'
                total += n + ((self.length - len(n)) * ' ') + ' |'
                total += '\n' + self.line('bot')
                return total

    def update_data(self):
        if self.hp <= 0:
            self.alive = False

        if not self.alive:
            if not self.name.lower().startswith('dead'):
                self.name = 'Dead %s' % self.name

        if self.max_hp + 4 > len(self.name) + 1:
            self.length = self.max_hp + 4
        else:
            self.length = len(self.name) + 1
