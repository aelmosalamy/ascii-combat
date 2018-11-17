'''
Contains various QoL functions which are used all over the game,
any text-based game would need such functions to satisfy the repetitive
need for simple stuff like: determining use "a" or "an" before item name
or placing some sentence inside a box, etc.. that is why "utils" exist
'''
from dicts import *
import time, os, platform

# Stores console's window size at launch
AC_SCREEN_WIDTH = 80
AC_SCREEN_HEIGHT = 35

# Console functions >
# Configures console's window size according to platform
def set_console_size():
    if platform.system() == 'Windows':
        os.system('title ASCII Combat')
        os.system('mode con: cols={} lines={}'.format(AC_SCREEN_WIDTH, AC_SCREEN_HEIGHT))
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        os.system('echo -n -e "\033]0;ASCII Combat\007"')
        os.system('resize -s {} {}'.format(AC_SCREEN_HEIGHT, AC_SCREEN_WIDTH))

# ASCII functions >
# Clears screen according to platform
def clear():
        print(C.Style.BRIGHT + C.Back.BLACK + C.Fore.WHITE, end='')
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')

# Returns an ANSI Sequence to change cursor position
def pos(x, y):
    return '\x1b[{};{}H'.format(int(y), int(x))

# Displays a nice looking banner, multi-lines are supported
def banner(text, corner='+', border='-'):
    max_length = 0
    _text = text.split('\n')
    # Checks max line length
    for line in _text:
        if len(line) > max_length:
            max_length = len(line)
    sides = corner + border * max_length + corner
    final_text = [sides]
    for line in _text:
        dif = 0
        if len(line) != max_length:
            dif = max_length - len(line)
        final_text.append('|{}{}|'.format(line, ' ' * dif))
    final_text.append(sides)
    return '\n'.join(final_text)

# Returns an empty screen with text in the middle
def center_screen(text):
    final = ''
    wspan = AC_SCREEN_WIDTH - 2
    final += '+' + '-' * wspan + '+'
    lines = text.split('\n')
    no_of_newlines = AC_SCREEN_HEIGHT - (len(lines) + 2)
    no_of_topnewlines = int(no_of_newlines / 2)
    final += no_of_topnewlines * ('|' + ' ' * wspan + '|\n')
    for line in lines:
        lnt = int((wspan - len(line)) / 2)
        final += '|' + ' ' * lnt + line + ' ' * lnt + '|' + '\n'
    no_of_botnewlines = no_of_newlines - no_of_topnewlines
    final += (no_of_botnewlines - 1) * ('|' + ' ' * wspan + '|\n')
    final += '|' + ' ' * wspan + '|'
    final += '+' + '-' * (AC_SCREEN_WIDTH-2) + '+'
    return final

# A transition between 2 scenes
def transition(time_in_seconds=3, text='Loading', phases=5):
    phase = 1
    while phase < phases + 1:
        clear()
        x = text + ' .' * phase + '\n'
        print(center_screen(x), end='')
        time.sleep(time_in_seconds / phases)
        phase += 1

# True if text start with vowel and vice versa
def use_an(text, capitalize = False):
    if text[0] in 'aeiou':
        a = 'an'
    else:
        a = 'a'
    if capitalize:
        a = list(a)
        a[0] = a[0].upper()
        a = ''.join(a)
    return a
    