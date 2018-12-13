from collections import namedtuple
from string import maketrans
INPUT = open("advent2018_day13_input.txt", "r").read().split("\n")
ALTINPUT = r'''
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
'''.split("\n")[1:]

DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
LEFT_DIRECTIONS = {'^': '<', '>': '^', 'v': '>', '<': 'v'}
RIGHT_DIRECTIONS = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

Coord = namedtuple('Coord', ['y', 'x'])


def go_in_direction(coord, direction):
    return Coord(x=coord.x+DIRECTIONS[direction][1], y=coord.y+DIRECTIONS[direction][0])


class Cart(object):
    TURNS = ["left", "straight", "right"]

    def __init__(self, direction=None, location=None):
        self.direction = direction
        self.location = location
        self.next_turn = 0
        self.crashed = False

    @property
    def left_direction(self):
        return LEFT_DIRECTIONS[self.direction]

    @property
    def right_direction(self):
        return RIGHT_DIRECTIONS[self.direction]

    def pick_new_direction(self):
        if self.next_turn == 0:
            new_direction = self.left_direction
        elif self.next_turn == 1:
            new_direction = self.direction
        elif self.next_turn == 2:
            new_direction = self.right_direction
        else:
            raise Exception("Shouldn't be here!  Unknown turn type")

        self.next_turn = (self.next_turn + 1) % 3
        return new_direction

    def __repr__(self):
        return "Cart(dir=%s, loc=%r, next_turn=%s)" % (self.direction, self.location, self.TURNS[self.next_turn])


def find_carts(field):
    carts = {}
    for i, line in enumerate(field):
        for j, column in enumerate(line):
            if column in ('^', 'v', '<', '>'):
                location = Coord(x=j, y=i)
                carts[location] = Cart(direction=column, location=location)
    return carts


def sanitize_carts(field):
    new_field = field[:]
    translation = maketrans('^v<>', '||--')
    for i, line in enumerate(new_field):
        new_field[i] = line.translate(translation)
    return new_field


def overlay_carts_on_field(field, cart_dict):
    new_field = field[:]
    for location, cart in cart_dict.iteritems():
        line = new_field[location.y]
        new_field[location.y] = line[:location.x] + cart.direction + line[location.x+1:]
    return new_field


def move_cart(field, cart, cart_locations):
    location_ahead = go_in_direction(cart.location, cart.direction)
    char_ahead = field[location_ahead.y][location_ahead.x]

    if location_ahead in cart_locations:
        cart.crashed = True
        new_direction = 'X'
    elif (char_ahead == '-' and cart.direction in ('>', '<')) or \
         (char_ahead == '|' and cart.direction in ('^', 'v')):
        new_direction = cart.direction
    elif (char_ahead == '\\' and cart.direction in ('^', 'v')) or \
         (char_ahead == '/' and cart.direction in ('<', '>')):
        new_direction = cart.left_direction
    elif (char_ahead == '/' and cart.direction in ('^', 'v')) or \
         (char_ahead == '\\' and cart.direction in ('<', '>')):
        new_direction = cart.right_direction
    elif char_ahead == "+":
        new_direction = cart.pick_new_direction()
    elif char_ahead == ' ':
        raise Exception("Shouldn't be here!  Cart tried to move off the track")
    else:
        raise Exception("Unknown combination of char %s and direction %s" % (char_ahead, cart.direction))
    return location_ahead, new_direction


def run_part_one(field, cart_dict, debug=False):
    if debug:
        print("1.")
        print("\n".join(overlay_carts_on_field(field, cart_dict)))
    iteration = 2
    while True:
        if debug:
            print("%d." % iteration)
        for _, cart in sorted(cart_dict.items(), key=lambda x: x[0]):
            new_location, new_direction = move_cart(field, cart, cart_dict.keys())
            del cart_dict[cart.location]
            cart.location = new_location
            cart.direction = new_direction
            cart_dict[new_location] = cart
            if cart.crashed:
                if debug:
                    print("\n".join(overlay_carts_on_field(field, cart_dict)))
                return cart.location
        if debug:
            print("\n".join(overlay_carts_on_field(field, cart_dict)))
        iteration += 1


def run_part_two(field, cart_dict, debug=False):
    if debug:
        print("1.")
        print("\n".join(overlay_carts_on_field(field, cart_dict)))
    iteration = 2
    while len(cart_dict) > 1:
        if debug:
            print("%d." % iteration)
        for _, cart in sorted(cart_dict.items(), key=lambda x: x[0]):
            if cart.crashed:
                continue
            new_location, new_direction = move_cart(field, cart, cart_dict.keys())
            del cart_dict[cart.location]
            if cart.crashed:
                cart_dict[new_location].crashed = True
                del cart_dict[new_location]
            else:
                cart.location = new_location
                cart.direction = new_direction
                cart_dict[new_location] = cart
        if debug:
            print("\n".join(overlay_carts_on_field(field, cart_dict)))
        iteration += 1
    # At this point we should only have one cart left
    return cart_dict[cart_dict.keys()[0]].location

field = INPUT
cart_dict = find_carts(field)
field = sanitize_carts(field)
crash_location = run_part_one(field, cart_dict)
print("Crash found at location %d,%d" % (crash_location.x, crash_location.y))

field = INPUT
cart_dict = find_carts(field)
field = sanitize_carts(field)
last_cart_location = run_part_two(field, cart_dict)
print("Last cart at location %d,%d" % (last_cart_location.x, last_cart_location.y))
