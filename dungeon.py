'''
This contains everything regarding the dungeon system, navigation, inventory
eating, looking, dropping and shop system, by far, the largest module in AC
'''
from dicts.utils import *
from dicts.rooms import *
from dicts.items import *
import player, combat, cmd, platform, os, textwrap
from time import sleep
from random import choice
import colorama as C

class Dungeon(cmd.Cmd):

    SCREEN_WIDTH = 80
    
    # Stores all coin items, so check_coins() can calculate difference between it
    # and any coin item in inventory, Adding the difference to self.coins
    old_coins_list = []
    last_item_picked = None

    inventory = ['apple', 'beef', 'sword', 'dagger']
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
    
    # (buy)
    NOT_SHOP = "There is nothing to buy from here, this isn't a shop"
    BUY_ITEM = "You successfully purchased"
    NO_MONEY = "You don't have enough coins for that item"
    NOT_SOLD_HERE = "That item isn't for sale, apparently."
    NO_ITEM_GIVEN_BUY = '<!!> What should I buy? e.g. "buy bread"'

    # combat
    MONSTER_CUT = ['A bunch of creepy monsters cut your path!', 'You take a step back, gazing at the overlooking beasts!',
    'Few evil-looking creatures gaze at you mockingly', 'Creepy, spooky enemies block your way',
    ]

    go_loadspeed = 2

    def __init__(self, player, rooms):
        super().__init__()
        # Windows requires init to use ANSI Sequences
        if platform.system() == 'Windows':
            C.init()
        # Initialising all variables
        self.location = 'town_square'
        self.current_room = ROOMS[self.location]
        self.coins = 0
        self.reset_color()
        self.player = player
        self.coin_hack(500) # Give me some money!
        self.rooms = rooms
        self.intro = input(center_screen(banner('''. . . <Welcome to ASCII Combat . . .
. . . Press Enter to Continue> . . .''')))
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

    # Pre/Post Loop functions
    def preloop(self):
        self.display_current_room()
    
    def postloop(self):
        pass

    # Utility functions
    # Converts any 'money' item in inventory to the user's 'coin' counter
    # based on the COIN_VALUE dictionary
    def check_coins(self):
        # Add all coin items in inventory to a temporary list
        updated_coins = [x for x in self.inventory if ITEMS[x][TAG] == 'coins']
        old_coins = list(self.old_coins_list)
        if len(updated_coins) > len(old_coins):
        # Checks for which coins are present in updated coins but
        # not present in our old coins then add it to self.coins
            for coin in updated_coins:
                if coin in old_coins:
                    old_coins.remove(coin)
                else:
                    self.coins += COIN_VALUE[coin]
                    self.old_coins_list.append(coin)
        elif len(updated_coins) < len(old_coins):
        # Check for old coins that are NOT present in our
        # updates coins and remove them from self.coins
            for coin in old_coins:
                if coin in updated_coins:
                    updated_coins.remove(coin)
                else:
                    self.coins -= COIN_VALUE[coin]
                    self.old_coins_list.remove(coin)

    # Easy coin hack, just specify the amount xD
    def coin_hack(self, amount):
        coins = ['coin'] * amount
        self.inventory += coins
        self.check_coins()

    @staticmethod
    def reset_color():
        print(C.Back.BLACK + C.Fore.WHITE + C.Style.BRIGHT, end='') 

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
        clear()
        self.check_coins()
        self.display_player_info()
        current_room = ROOMS[self.location]
        # Displays current room name
        print(C.Fore.YELLOW + banner(current_room[NAME], border='~'))
        self.reset_color()
        # Displays room's USERDESC + DESC
        room_desc = self.PROMPT_SIGN + current_room[USERDESC] + ' ' + current_room[DESC]
        # Different experience if first time entry
        if current_room[SEEN]:
            print('\n'.join(textwrap.wrap(room_desc, self.SCREEN_WIDTH)))
        else:
            # Slowly writes room description
            typewriter('\n'.join(textwrap.wrap(room_desc, self.SCREEN_WIDTH)))
            # Sets the destination as SEEN
            self.room_seen(self.location)
        self.reset_color()
        print('\n')
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
        x = 5 + len("[{}] [HP] {}/{}[Weapon] {}[Skill] {}[Coins] {}$".format(p.name, p.hp, p.max_hp,
        p.weapon, p.skill_type[NAME], self.coins))
        # Printing top border
        print('\{}┌{}┐   /'.format(' ' * (EXTENSION + 1), '-' * x))
        # Printing colored stats
        c_user_stats = "{}[{}] {}[HP] {}/{} {}[Weapon] {} {}[Skill] {} {}[Coins] {}$".format(
        C.Fore.CYAN, p.name,
        C.Fore.GREEN, p.hp, p.max_hp, 
        C.Fore.RED, p.weapon, 
        C.Fore.MAGENTA, p.skill_type[NAME],
        C.Fore.YELLOW, self.coins)
        print(' \{}| {}{} {}'.format('_' * EXTENSION, c_user_stats, C.Fore.WHITE, '|__/'))
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

    # Dramatically prompts user to accept fight, returns True if accepted False if retreat chosen
    def ask_fight_or_flight(self, target_room, dir):
        
        sleep(2)
        clear()
        print(RED + center_screen('While going ' + dir + ', to ' + target_room[NAME] + ' . . .'), end='')
        sleep(3)

        clear()
        print(RED + center_screen(choice(self.MONSTER_CUT) + ' . . .'), end='')
        sleep(4)

        clear()
        print(RED + center_screen("You don't know how many are there, but you know . . ."), end='')
        sleep(2)
        
        clear()
        print(RED + center_screen("That if you are going to fight, It will be you. And you only . . ."), end='')
        sleep(3)

        clear()
        print(WHITE + center_screen("Will you face your enemies, or . . run away?"), end='')
        sleep(4)

        print(WHITE)
        while True:
            clear()
            answer = input(banner("Fight or Flight!") + '\n\n' + self.PROMPT_SIGN + 'Do you accept this deadly fight [y/n]?\n' + BULLET)
            # Fight, enter combat
            if answer.lower() == 'y':
                # Accepted fight, Choosing weapons/skill and more!
                clear()
                print(C.Fore.RED + "> PREPARING FOR FIGHT <")
                print('=' * 23)
                my_weapons = get_tag_items(self.inventory, 'weapon')
                if my_weapons:
                    # Selecting weapon to use
                    print(self.PROMPT_SIGN + ' Pick your weapon:')
                    for weapon in my_weapons:
                        print(weapon)
                else:
                    # No weapons
                    print(self.PROMPT_SIGN + "Your fist is your only weapon!")
        
                return True
            # Flight, return to previous room
            elif answer.lower() == 'n':
                return False

    # Sorts items in a list of items (particularly self.inventory) according
    # to tags and prints them
    def sort_inventory_items(self, item_names):
        l = 7 # Length of 'Name  | ' to be used as indent
        # Tracks displayed items, so they are not repeated
        displayed_items = [] 
        # key is a lowercase tag (for comparison with item tags)
        # value is a decorated text for display
        tags = {tag:tag[0].upper() + tag[1:] + (l - len(tag)) * ' ' + '| ' for tag in INVENTORY_TAGS}
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
                    x = '{}({})'.format(item[NAME], item_count)
                # Highlights item name if it just got picked last turn
                if item_name == self.last_item_picked:
                    x = C.Fore.YELLOW + x + WHITE
                # Display the item if it is in inventory tags
                if item[TAG] in INVENTORY_TAGS:
                    tags[item[TAG]] += WHITE + x + CYAN + SEP + WHITE
                displayed_items.append(item_name)
        # Support for big inventories with textwrap
        # This to indent every single line except the first line which is printed
        # independently, since it contains the title 'Food  |', then other lines are indented
        for tag in tags.values():
            _tag = textwrap.wrap(tag, self.SCREEN_WIDTH + 43)
            print(HIGHLIGHT_COLOR + _tag[0])
            _tag.remove(_tag[0])
            for line in _tag:
                print(' ' * (l + 2) + line) 
        print()

    # Prints an ASCII map of all rooms
    def graph_rooms(self):
        # TO BE IMPLEMENTED
        pass

    # Checks a room as seen
    @staticmethod
    def room_seen(room_id):
        ROOMS[room_id][SEEN] = True

    # Follows a given direction to move from current location to a new location
    def go_new_location(self, inp):
        current_room = ROOMS[self.location]
        # Checks all DIRECTIONS, comparing them to user input
        for dir in DIRECTIONS:
            # If the DESTINATION is available and matches user input, move to it
            if current_room[dir] and dir == inp:
                target_room_id = current_room[dir]
                # Finds approperiate wording for the load screen!
                if inp == UP: load_text='Climbing'
                elif inp == DOWN: load_text='Descending'
                else: load_text = 'Walking'
                # Loader between screens
                transition(self.go_loadspeed, text=load_text + ' ' + inp + '!')
                # If target room contains enemies, prompt for combat
                if ROOMS[target_room_id][ENEMIES]:
                    # If fight
                    if self.ask_fight_or_flight(ROOMS[target_room_id], dir):
                        pass
                    # If user chose retreat
                    else:
                        transition(text='Retreating cowardly to ' + current_room[NAME])
                        self.display_current_room()
                # Elif room is peaceful, change location and display room
                else:
                    self.location = current_room[dir]
                    self.display_current_room()
            # If the DESTINATION is empty
            elif dir == inp and not current_room[dir]:
                self.display_current_room()
                # Customized messages for CLIMBING/DESCENDING no destination
                if dir == UP:
                    self.error_msg(self.NO_UP)
                elif dir == DOWN:
                    self.error_msg(self.NO_DOWN)
                # N/S/E/W
                else:
                    self.error_msg('{} {}'.format(self.EMPTY_DIR, dir.upper()))

    # Generates a new dungeon structure using existing rooms
    def generate_dungeon(self, room_list):
        pass

    # Cmd commands
    # Navigate in a specific direction
    def do_go(self, arg):
        # If input is an actual DIRECTION
        if arg.lower() in DIRECTIONS:
            # Go to new location, If enemies present ask for fight/flight
            self.go_new_location(arg.lower())
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
        # If input is one of the items in ground, shop, inventory
        all_items = current_room[GROUND] + current_room[SHOP] + self.inventory
        if arg.lower() in all_items:
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
                # Remove item from ground, Add to inventory, Display it to user
                current_room[GROUND].remove(item[NAME].lower())
                self.inventory.append(item[NAME].lower())
                self.last_item_picked = item[NAME].lower()
                self.display_current_room()
                self.achieve_msg('{} {} {}'.format(self.PICK_ITEM[0],
                HIGHLIGHT_COLOR + item[NAME].lower() + CYAN,
                self.PICK_ITEM[1]))
            else:
                # Error: Item NOT pickable
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
    
    def do_buy(self, arg):
        current_room = ROOMS[self.location]
        # THIS IS A SHOP AND YOU CAN INTERACT WITH IT
        if current_room[SHOP]:
            if arg.lower() in current_room[SHOP]:
                price = ITEMS[arg.lower()][PRICE]
                if self.coins >= price:
                    self.coins -= price
                    self.inventory.append(arg.lower())
                    x = '{} {} for {}$'.format(self.BUY_ITEM,
                    HIGHLIGHT_COLOR + arg.lower() + CYAN, C.Fore.YELLOW + str(price))
                    self.last_item_picked = arg.lower()
                    self.display_current_room()
                    self.achieve_msg(x)
                else:
                    # YOU CANT BUY THIS ITEM, YOU GOT NO MONEY
                    self.error_msg(self.NO_MONEY)
            # Empty input
            elif not arg:
                self.error_msg(self.NO_ITEM_GIVEN_BUY)
            # THE ITEM YOU WANT IS NOT FOR SALE
            elif arg.lower() not in current_room[SHOP]:
                self.error_msg(self.NOT_SOLD_HERE)
        else:
            # THIS ISNT A SHOP
            self.display_current_room()
            self.error_msg(self.NOT_SHOP)

if __name__ == '__main__':
    me = player.Player('Bori', 10, WEAPONS[FIST])
    world = Dungeon(me, ROOMS)
    world.cmdloop()