from ac_dicts import *
import player, combat, cmd, platform, os
import colorama as C

class Dungeon(cmd.Cmd):

    location = 'town_square'
    current_room = ROOMS[location]

    inventory = []
    
    PROMPT_SIGN = '# '
    UNKNOWN_CMD = 'What do you mean by that?'
    PROMPT_MSG = 'Would you like to: <go>? <pick>? <look>? <eat>?\n> '
    EMPTY_DIR = 'There is nothing found miles away towards'
    BAD_DIR = '''I dont think this direction can be found on any compass!
Check these, perhaps? NORTH/SOUTH/EAST/WEST or UP/DOWN'''
    NO_DIR_GIVEN = 'Please tell me where do you want to go!'
    NO_UP = "You can't climb UP, and I don't believe you can fly anyway!"
    NO_DOWN = "There is no secret staircase DOWN here, except if you are good at digging!"

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

    # Displays an error prompts, supports multi-line prompts
    def error_msg(self, text):
        self.display_current_room()
        print(C.Back.RED + C.Fore.RED, end='')
        _text = text.split('\n')
        for line in _text:
            print(self.PROMPT_SIGN + line)
        self.reset_color()

    def achieve_msg(self, text):
        self.display_current_room()
        print(C.Back.CYAN + C.Fore.CYAN, end='')
        _text = text.split('\n')
        for line in _text:
            print(self.PROMPT_SIGN + line)
        self.reset_color()

    # Prints information about the current room
    def display_current_room(self):
        self.clear()
        # Displays room description
        current_room = ROOMS[self.location]
        print(C.Fore.YELLOW, end='')
        print(banner(current_room[NAME], border='~'))
        self.reset_color()
        print(self.PROMPT_SIGN + current_room[USERDESC] + '\n' + current_room[DESC])
        self.reset_color()
        print()
        # Displays all items on the ground
        print(get_items_grounddesc(current_room))
        # Displays exits with colors
        for k, v in get_room_exits(current_room).items():
            print('{}{}{}| {}{}'.format(C.Fore.MAGENTA, k.upper(), (5 - len(k)) * ' ', C.Fore.CYAN, v))
        print()
        self.reset_color()
        
    # Prints an ASCII map of all rooms
    def display_rooms(self):
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

if __name__ == '__main__':
    me = player.Player('Bori', 10, WEAPONS[DAGGER])
    world = Dungeon(me, ROOMS)
    world.cmdloop()