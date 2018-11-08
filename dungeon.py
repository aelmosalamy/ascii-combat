from ac_dicts import *
import player, combat, cmd, platform, os, textwrap
import colorama as C

class Dungeon(cmd.Cmd):

    SCREEN_WIDTH = 80

    location = 'town_square'
    current_room = ROOMS[location]

    inventory = ['apple', 'fountain', 'dagger', 'cake', 'apple', 'bread']
    
    PROMPT_SIGN = '# '
    INV_INTRO = '[INVENTORY]'
    UNKNOWN_CMD = 'What do you mean by that?'
    PROMPT_MSG = 'Would you like to: <go>? <pick>? <look>? <eat>?\n> '
    EMPTY_DIR = 'There is nothing found miles away towards'
    BAD_DIR = '''I dont think this direction can be found on any compass!
Check these, perhaps? NORTH/SOUTH/EAST/WEST or UP/DOWN'''
    NO_DIR_GIVEN = 'Please tell me where do you want to go! e.g. "go north"'
    NO_UP = "You can't climb UP, and I don't believe you can fly anyway!"
    NO_DOWN = "There is no secret staircase DOWN here, except if you are good at digging!"
    BAD_ITEM = "I can't see that item anywhere in here!"
    NO_ITEM_GIVEN = 'What should I look at? e.g. "look apple"'

    def __init__(self, player, rooms):
        super().__init__()
        if platform.system() == 'Windows':
            C.init()
        self.reset_color()
        self.player = player
        self.rooms = rooms
        self.intro = input(banner('. . . Welcome to ASCII Combat . . .\n. . . Press Enter to Continue . . .'))
        self.prompt = self.PROMPT_SIGN + self.PROMPT_MSG
    
    # cmd.Cmd functions overriding
    # Avoids repitition of last command
    def emptyline(self):
        self.display_current_room()

    # Error message for unknown commands
    def default(self, line):
        self.display_current_room()
        self.error_msg('{}!? {}'.format(line, self.UNKNOWN_CMD))
    
    # Removes the help method
    def do_help(self, arg):
        self.display_current_room()

    # Controls termination of Combat
    def postcmd(self, stop, line):
        pass

    # Pre/Post Loop functions
    def preloop(self):
        self.display_current_room()

    # Utility functions
    @staticmethod
    def reset_color():
        print(C.Back.BLACK + C.Fore.WHITE + C.Style.BRIGHT, end='')

    @staticmethod
    def clear():
        print(C.Style.BRIGHT + C.Back.BLACK + C.Fore.WHITE, end='')
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')

    # Displays an error prompt, supports multi-line prompts
    def error_msg(self, text):
        self.display_current_room()
        print(C.Back.RED + C.Fore.BLACK, end='')
        _text = text.split('\n')
        for line in _text:
            print(self.PROMPT_SIGN + line)
        self.reset_color()

    # Displays an achievement/notification, supports multi-line prompts
    def achieve_msg(self, text, wrap=False):
        print(C.Back.CYAN + C.Fore.BLACK, end='')
        if wrap:
            _text = textwrap.wrap(text, self.SCREEN_WIDTH - len(self.PROMPT_SIGN))
            for line in _text:
                print(self.PROMPT_SIGN + line)
        else: print(self.PROMPT_SIGN, text)
        self.reset_color()

    # Prints information about the current room
    def display_current_room(self):
        self.clear()
        self.display_player_info()
        # Displays room description
        current_room = ROOMS[self.location]
        print(C.Fore.YELLOW, end='')
        print(banner(current_room[NAME], border='~'))
        self.reset_color()
        room_desc = self.PROMPT_SIGN + current_room[USERDESC] + '. ' + current_room[DESC]
        for line in textwrap.wrap(room_desc, self.SCREEN_WIDTH):
            print(line)
        self.reset_color()
        print()
        # Displays all items on the ground
        print(get_items_grounddesc(current_room))
        # Displays exits with colors
        for k, v in get_room_exits(current_room).items():
            print('{}{}{}| {}{}'.format(C.Fore.MAGENTA, k.upper(), (5 - len(k)) * ' ', C.Fore.CYAN, v))
        print()
        self.reset_color()
    
    # Prints user info
    def display_player_info(self):
        p = self.player
        # This long solution (instead of using "banner()") is done because len() function
        # deals with ANSI escape sequences as an actual string (while it is not actually
        # seen by the user) so this is a simple workaround
        EXTENSION = 2 # This controls how long the left handle for the banner is
        x = 6 + len("[{}] [HP] {}/{}[Weapon] {}[Skill] {}".format(p.name, p.hp, p.max_hp, p.weapon, p.skill_type[NAME]))
        # Printing top border
        print('\{}┌{}┐        /'.format(' ' * (EXTENSION + 1), '-' * x))
        # Printing colored stats
        c_user_stats = "{}[{}] {}[HP] {}/{} {}[Weapon] {} {}[Skill] {}".format(
        C.Fore.CYAN, p.name,
        C.Fore.GREEN, p.hp, p.max_hp, 
        C.Fore.RED, p.weapon, 
        C.Fore.MAGENTA, p.skill_type[NAME])
        print(' \{}| {}{} {}'.format('_' * EXTENSION, c_user_stats, C.Fore.WHITE, '  |_______/'))
        # Print bot border
        print(' ' * (EXTENSION + 2) + '└' + '-' * x + '┘')
        self.display_inventory()

    # Prints user's inventory
    def display_inventory(self):
        print()
        print('  ' + C.Fore.YELLOW + self.INV_INTRO)
        # print('    ' + len(self.INV_INTRO) * '=') Underlines inventory string
        self.reset_color()
        print(sort_inventory_items(self.inventory))

    # Prints an ASCII map of all rooms
    def graph_room(self):
        pass

    # Follows a given direction to move from current location to a new location
    def go_new_location(self, input):
        current_room = ROOMS[self.location]
        # Checks all DIRECTIONS, comparing them to user input
        for dir in DIRECTIONS:
            # If the DESTINATION is available, move to it
            if current_room[dir] and dir == input.lower():
                self.location = current_room[dir]
                self.display_current_room()
            # If the DESTINATION is empty
            elif dir == input.lower() and not current_room[dir]:
                self.display_current_room()
                # Customized messages for CLIMBING/DESCENDING no destination
                if dir == UP:
                    self.error_msg(self.NO_UP)
                elif dir == DOWN:
                    self.error_msg(self.NO_DOWN)
                # N/S/E/W
                else:
                    self.error_msg('{} {}'.format(self.EMPTY_DIR, dir.upper()))

    # Cmd commands
    # Navigate in a specific direction
    def do_go(self, arg):
        # If input is an actual DIRECTION
        if arg.lower() in DIRECTIONS:
            self.go_new_location(arg)
        # Empty input
        elif not arg:
            self.display_current_room()
            self.error_msg(self.NO_DIR_GIVEN)
        # If input is not a valid DIRECTION
        elif arg.lower() not in DIRECTIONS:
            self.display_current_room()
            self.error_msg(self.BAD_DIR)
    
    # Look at something (Display its LONGDESC)
    def do_look(self, arg):
        current_room = ROOMS[self.location]
        # If input is one of the items on ground
        if arg.lower() in current_room[GROUND]:
            item = ITEMS[arg.lower()]
            self.display_current_room()
            self.achieve_msg(item[LONGDESC], wrap = True)
        # Empty input
        elif not arg:
            self.display_current_room()
            self.error_msg(self.NO_ITEM_GIVEN)
        elif arg.lower() not in current_room[GROUND]:
            self.display_current_room()
            self.error_msg(self.BAD_ITEM)

if __name__ == '__main__':
    me = player.Player('Bori', 10, WEAPONS[DAGGER])
    world = Dungeon(me, ROOMS)
    world.cmdloop()