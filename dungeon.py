from ac_dicts import *
import player, combat, cmd, platform, os, textwrap
import colorama as C

class Dungeon(cmd.Cmd):

    SCREEN_WIDTH = 80

    location = 'bakery'
    current_room = ROOMS[location]
    coins = 0
    last_item_picked = None

    inventory = ['apple']
    PROMPT_SIGN = '# '

    # String constants used for user interaction, They are supposed to be written
    # in First-Person, some strings are placed in a list for those scenarios: 
    # 1. An item name will be inserted in the middle
    # 2. Multiple versions of same context to add variety to the dialogue (Nobody likes repitition)
    # main loop
    INV_INTRO = 'Pockets'
    EMPTY_INV = 'Your pockets are empty . . .\n'
    UNKNOWN_CMD = 'What do you mean by that?'
    PROMPT_MSG = 'Would you like to: <go>? <look>? <pick>? <drop>? <eat>?\n> '
    ROOM_FULL = "This room can't take more, find somewhere else to drop your stuff!"
    # general
    BAD_ITEM = "I can't see that item anywhere in here!"
    UNKNOWN_ITEM = "!? What on earth is that? Never seen nor heared of such an item before"
    # (go)
    EMPTY_DIR = 'There is nothing found miles away towards'
    BAD_DIR = '''I dont think this direction can be found on any compass!
Check these, perhaps? NORTH/SOUTH/EAST/WEST or UP/DOWN'''
    NO_DIR_GIVEN = '<!!> Where should I go? e.g. "go north"'
    NO_UP = "You can't climb UP, and I don't believe you can fly anyway!"
    NO_DOWN = "There is no secret staircase DOWN here, except if you are good at digging!"
    # (look)
    NO_ITEM_GIVEN = '<!!> What should I look at? e.g. "look apple"'
    PICK_ITEM = ['You stuff that', 'in your can-hold-everything pocket']
    # (pick)
    NO_ITEM_GIVEN_PICK = '<!!> What should I pick? e.g. "pick apple"'
    NOT_PICKABLE = ["I am afraid you can't take that", "with you, It belongs here!"]
    # (eat)
    BAD_FOOD = "would be delicious, unfortunately I don't have one"
    NO_ITEM_GIVEN_EAT = '<!!> I would like to eat, but what should I eat!? e.g. "eat apple"'
    NOT_EDIBLE = [
    ['They call me "Shark Teeth", but still this', 'is too hard for me to eat'],
    ['I might suffocate eating this', ''],
    ['Only a mad person would eat a', 'gladly I am not that guy'],
    ['I am not sure if this', 'is edible, better not try']
    ]
    SWALLOW_SYNONYMS = ['consume', 'devour', 'gulp down', 'eat', 'swallow', 'feast on']

    # (drop)
    NO_ITEM_GIVEN_DROP = '<!!> What should I drop? e.g. "drop apple"'
    BAD_DROP = "You cann't get rid of something you dont actually own"

    def __init__(self, player, rooms):
        super().__init__()
        if platform.system() == 'Windows':
            C.init()
        self.reset_color()
        self.player = player
        self.rooms = rooms
        self.intro = input(banner('. . . Welcome to ASCII Combat . . .\n. . . Press Enter to Continue . . .'))
        self.prompt = self.PROMPT_SIGN + self.PROMPT_MSG
        self.INV_INTRO = "[{}'s {}]".format(self.player.name, self.INV_INTRO)
    
    # cmd.Cmd functions overriding
    # Avoids repitition of last command
    def emptyline(self):
        self.display_current_room()

    # Error message for unknown commands
    def default(self, line):
        self.display_current_room()
        self.error_msg('"{}"!? {}'.format(line, self.UNKNOWN_CMD))
    
    # Removes the help method
    def do_help(self, arg):
        self.display_current_room()

    # Controls termination of Combat
    def postcmd(self, stop, line):
        pass

    # Pre/Post Loop functions
    def preloop(self):
        self.check_coins()
        self.display_current_room()

    # Utility functions
    # Converts any 'money' item in inventory to the user's 'coin' counter
    # based on the COIN_VALUE dictionary
    def check_coins(self):
        # Initializes coins
        self.coins = 0
        my_coins = [x for x in self.inventory if ITEMS[x][TAG] == 'coins']
        for coin in my_coins:
            self.coins += COIN_VALUE[coin]

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
    def error_msg(self, text, wrap = True):
        self.display_current_room()
        print(C.Fore.RED, end='')
        if wrap:
            _text = textwrap.wrap(text, self.SCREEN_WIDTH - len(self.PROMPT_SIGN))
            for line in _text:
                print(self.PROMPT_SIGN + line)
        else: 
            print(self.PROMPT_SIGN + text)
        self.reset_color()

    # Displays an achievement/notification, supports multi-line prompts
    def achieve_msg(self, text, wrap=False):
        print(C.Back.BLUE + C.Fore.CYAN, end='')
        if wrap:
            _text = textwrap.wrap(text, self.SCREEN_WIDTH - len(self.PROMPT_SIGN))
            for line in _text:
                print(self.PROMPT_SIGN + line)
        else: 
            print(self.PROMPT_SIGN + text)
        self.reset_color()

    # Prints information about the current room
    def display_current_room(self):
        self.clear()
        self.check_coins()
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
        # Displays all items for sale at the shop
        if current_room[SHOP]:
            ln = 20
            print(self.PROMPT_SIGN + current_room[SHOPINTRO] + '\n')
            for item_name in current_room[SHOP]:
                item = ITEMS[item_name]
                lnp = len(str(item[PRICE]))
                print('{}{} {}{}{}({}$)'.format(BULLET, HIGHLIGHT_COLOR + item[NAME] + WHITE,
                '-' * (ln - len(item[NAME])), C.Fore.YELLOW, ' ' * (3 - lnp), item[PRICE]))
                self.reset_color()
            print()
        else:
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
        EXTENSION = 1 # This controls how long the left handle for the banner is
        x = 5 + len("[{}] [HP] {}/{}[Weapon] {}[Skill] {}[Coins] {}".format(p.name, p.hp, p.max_hp,
        p.weapon, p.skill_type[NAME], self.coins))
        # Printing top border
        print('\{}┌{}┐     /'.format(' ' * (EXTENSION + 1), '-' * x))
        # Printing colored stats
        c_user_stats = "{}[{}] {}[HP] {}/{} {}[Weapon] {} {}[Skill] {} {}[Coins] {}".format(
        C.Fore.CYAN, p.name,
        C.Fore.GREEN, p.hp, p.max_hp, 
        C.Fore.RED, p.weapon, 
        C.Fore.MAGENTA, p.skill_type[NAME],
        C.Fore.YELLOW, self.coins)
        print(' \{}| {}{} {}'.format('_' * EXTENSION, c_user_stats, C.Fore.WHITE, '|____/'))
        # Print bot border
        print(' ' * (EXTENSION + 2) + '└' + '-' * x + '┘')
        self.display_inventory()

    # Prints user's inventory
    def display_inventory(self):
        print()
        print('  ' + C.Fore.YELLOW + self.INV_INTRO)
        # print('    ' + len(self.INV_INTRO) * '=') Underlines inventory string
        self.reset_color()
        if self.inventory:
            self.sort_inventory_items(self.inventory)
        else:
            print('  ' + self.EMPTY_INV)

    # Sorts items in a list of items (particularly self.inventory) according
    # to tags and prints them
    def sort_inventory_items(self, item_names):
        l = 9 # Length of 'Name  | ' to be used as indent
        displayed_items = []
        food_tag   = CYAN + 'Food   | '
        weapon_tag = CYAN + 'Weapons| '
        random_tag  = CYAN + 'Random | '
        for item_name in item_names:
        # If that item got already displayed dont print second ocurrences
            if item_name in displayed_items: 
                pass
            else:
                item_count = item_names.count(item_name)
                item = ITEMS[item_name]
                # Prints item count if there is more than one of that item
                if item_count == 1:
                    x = item[NAME]
                elif item_count > 1:       
                    x = '{} ({})'.format(item[NAME], item_count)
                # Highlights item name if it just got picked last turn
                if item_name == self.last_item_picked:
                    x = C.Fore.YELLOW + x + WHITE
                if item[TAG] == 'food':
                    food_tag += WHITE + x + CYAN + SEP + WHITE
                elif item[TAG] == 'weapon':
                    weapon_tag += WHITE + x + CYAN + SEP + WHITE
                elif item[TAG] == 'random':
                    random_tag += WHITE + x + CYAN + SEP + WHITE
                # Our item is displayed with count, add it to displayed_items
                displayed_items.append(item_name)
        # Support for big inventories with textwrap
        # This to indent every single line except the first line which is printed
        # independently, since it contains the title 'Food  |', then other lines are indented
        # FOOD LINE
        _food = textwrap.wrap(food_tag, self.SCREEN_WIDTH + 43)
        print(_food[0])
        _food.remove(_food[0])
        for line in _food:
            print(' ' * l + line)
        # WEAPON LINE
        _weapon = textwrap.wrap(weapon_tag, self.SCREEN_WIDTH + 43)
        print(_weapon[0])
        _weapon.remove(_weapon[0])
        for line in _weapon:
            print(' ' * l + line)
        # random LINE
        _random = textwrap.wrap(random_tag, self.SCREEN_WIDTH + 43)
        print(_random[0])
        _random.remove(_random[0])
        for line in _random:
            print(' ' * l + line)      
        print()

    # Prints an ASCII map of all rooms
    def graph_rooms(self):
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
            if arg.lower() in ITEMS:
                self.display_current_room()
                self.error_msg(self.BAD_ITEM)
            else:
                self.display_current_room()
                self.error_msg('"{}"{}'.format(arg, self.UNKNOWN_ITEM))
            
    
    # Pick an item (Remove it from ROOM[GROUND] add it to self.inventory)
    def do_pick(self, arg):
        current_room = ROOMS[self.location]
        # If input is one of the items on ground
        if arg.lower() in current_room[GROUND]:
            item = ITEMS[arg.lower()]
            # Pick if item is PICKABLE otherwise ERRORRRRR!!!
            if item[PICKABLE]:
                # Add item to inventory after removing it from ground then display
                current_room[GROUND].remove(item[NAME].lower())
                self.inventory.append(item[NAME].lower())
                self.check_coins()
                self.last_item_picked = item[NAME].lower()
                self.display_current_room()
                self.achieve_msg('{} {} {}'.format(self.PICK_ITEM[0],
                HIGHLIGHT_COLOR + item[NAME].lower() + CYAN,
                self.PICK_ITEM[1]))
            else:
                self.display_current_room()
                self.error_msg('{} {} {}'.format(self.NOT_PICKABLE[0],
                HIGHLIGHT_COLOR + item[NAME].lower() + C.Fore.RED, self.NOT_PICKABLE[1]))
        # Empty input
        elif not arg:
            self.display_current_room()
            self.error_msg(self.NO_ITEM_GIVEN_PICK)
        elif arg.lower() not in current_room[GROUND]:
            if arg.lower() in ITEMS:
                self.display_current_room()
                self.error_msg(self.BAD_ITEM)
            else:
                self.display_current_room()
                self.error_msg('"{}"{}'.format(arg, self.UNKNOWN_ITEM))

    
    # Eat an item (Remove it from invetory)
    def do_eat(self, arg):
        # If input is found in inventory
        if arg.lower() in self.inventory:
            if ITEMS[arg.lower()][EDIBLE] == True:
                # Generate a "You swallow-synonym that item" string
                x = 'You {} that {}{}{}'.format(choice(self.SWALLOW_SYNONYMS), HIGHLIGHT_COLOR,
                arg.lower(), WHITE)
                # Remove item from inventory then display room
                self.inventory.remove(arg.lower())
                self.display_current_room()
                self.achieve_msg(x)
            else:
                # Prints a funny prompt if item is not edible
                s = choice(self.NOT_EDIBLE)
                self.display_current_room()
                self.achieve_msg(s[0] + ' {}{}{} '.format(HIGHLIGHT_COLOR, arg.lower(), CYAN) + s[1])
        # Empty input
        elif not arg:
            self.display_current_room()
            self.error_msg(self.NO_ITEM_GIVEN_EAT)
        # If item isn't in inventory check if such item exists and prompt accordingly
        elif arg.lower() not in self.inventory:
            if arg.lower() in ITEMS:
                self.display_current_room()
                x = '{} {}{}{} {}'.format(use_an(arg.lower(), True), HIGHLIGHT_COLOR, arg.lower(), C.Fore.RED, self.BAD_FOOD)
                self.error_msg(x)
            else:
                self.display_current_room()
                self.error_msg('"{}"{}'.format(arg, self.UNKNOWN_ITEM))
    
    # Drops an item (Remove it from inventory, add it to current_room's GROUND)
    def do_drop(self, arg):
        current_room = ROOMS[self.location]
        # If input is found in inventory
        if arg.lower() in self.inventory:
            # Prints that you dropped an item
            x = 'You dropped ' + use_an(arg.lower()) + ' ' + HIGHLIGHT_COLOR + arg.lower() + WHITE
            # Remove item from inventory then display room
            if len(current_room[GROUND]) < GROUND_LIMIT:
                self.inventory.remove(arg.lower())
                current_room[GROUND].append(arg.lower())
                self.display_current_room()
                self.achieve_msg(x)
            else:
                self.display_current_room()
                self.error_msg(self.ROOM_FULL)
        # Empty input
        elif not arg:
            self.display_current_room()
            self.error_msg(self.NO_ITEM_GIVEN_DROP)
        # If item isn't in inventory check if such item exists and prompt accordingly
        elif arg.lower() not in self.inventory:
            if arg.lower() in ITEMS:
                # I WOULD LIKE TO EAT THAT
                self.display_current_room()
                self.error_msg(self.BAD_DROP)
            else:
                # WTH IS THAT ITEM? NEVER HEARD OF IT
                self.display_current_room()
                self.error_msg('"{}"{}'.format(arg, self.UNKNOWN_ITEM))

if __name__ == '__main__':
    me = player.Player('Bori', 10, WEAPONS[DAGGER])
    world = Dungeon(me, ROOMS)
    world.cmdloop()