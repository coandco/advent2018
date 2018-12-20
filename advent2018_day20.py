from collections import namedtuple, defaultdict
import sre_parse
import re

INPUT = open("advent2018_day20_input.txt", "r").read()

ALTINPUT = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"
ALTINPUT_2 = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
ALTINPUT_3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"

Coord = namedtuple('Coord', ['y', 'x'])

DIRECTIONS = {'N': Coord(x=0, y=-1), 'E': Coord(x=1, y=0), 'S': Coord(x=0, y=1), 'W': Coord(x=-1, y=0)}
OPPOSITE_DIRECTIONS = {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}


def go_direction(coord, direction):
    return Coord(x=coord.x+DIRECTIONS[direction].x, y=coord.y+DIRECTIONS[direction].y)


class Room(object):
    def __init__(self, location, shortest_path=None):
        self.location = location
        self.shortest_path = shortest_path if shortest_path else ''
        self.doors = {'N': False, 'E': False, 'S': False, 'W': False}

    @property
    def shortest_path_len(self):
        return len(self.shortest_path)


class Frame(object):
    def __init__(self, loc, path):
        self.loc = loc
        self.path = path

    def copy(self):
        return Frame(self.loc, self.path)

    def __repr__(self):
        return "Frame(x,y=%d,%d path=%s)" % (self.loc.x, self.loc.y, self.path)


# This is a very naive solution that only works because of a couple unstated constraints in the given input.
# 1. Unlike the examples in the problem, you will never have bifurcation of paths like ^N(E|W)N$.  Instead,
#    the only time you'll have additional directions after a ) is after a set that returns back on itself,
#    like ^N(NWES|)N$.
# 2. Sets with an empty option like (NWES|) will always have exactly one option that backtracks fully, and
#    will have no recursion inside themselves.
def parse_paths(paths_str):
    rooms = {}
    cur_loc = Coord(x=0, y=0)
    rooms[cur_loc] = Room(cur_loc, shortest_path='')

    frames = []
    cur_frame = Frame(cur_loc, '')
    # Strip off the ^ and $ from paths_str
    for char in paths_str[1:-1]:
        if char in (DIRECTIONS.keys()):
            rooms[cur_frame.loc].doors[char] = True
            cur_frame.path += char
            cur_frame.loc = go_direction(cur_frame.loc, char)
            if cur_frame.loc not in rooms.keys():
                new_room = Room(cur_frame.loc, shortest_path=cur_frame.path)
                rooms[cur_frame.loc] = new_room
            else:
                new_room = rooms[cur_frame.loc]
            if len(cur_frame.path) < len(new_room.shortest_path):
                new_room.shortest_path = cur_frame.path
            new_room.doors[OPPOSITE_DIRECTIONS[char]] = True
        elif char == '(':
            frames.append(cur_frame.copy())
        elif char == '|':
            cur_frame = frames[-1].copy()
        elif char == ')':
            cur_frame = frames.pop()

    return rooms


# Not strictly necessary, but was useful for debugging
def print_maze(rooms):
    y_vals, x_vals = zip(*rooms.keys())
    x_max, y_max = max(x_vals), max(y_vals)
    x_min, y_min = min(x_vals), min(y_vals)
    for i in xrange(y_min, y_max + 1):
        row_lines = ['', '', '']
        for j in xrange(x_min, x_max + 1):
            cur_loc = Coord(x=j, y=i)
            cur_room = rooms[cur_loc] if cur_loc in rooms.keys() else Room(cur_loc)
            middle = '  X  ' if cur_loc == Coord(x=0, y=0) else "%05d" % cur_room.shortest_path_len
            row_lines[0] += "###{}###".format('-' if cur_room.doors['N'] else '#')
            row_lines[1] += '{}{}{}'.format('|' if cur_room.doors['W'] else '#', middle,
                                            '|' if cur_room.doors['E'] else '#')
            row_lines[2] += "###{}###".format('-' if cur_room.doors['S'] else '#')
        print("\n".join(row_lines))


# This is a very hacky solution which I'm surprised works
def part_one(input):
    shrunk_input = re.sub(r'\([NSEW]+\|\)', '', input)
    return sre_parse.parse(shrunk_input).getwidth()[1]


def part_two(input):
    rooms = parse_paths(input)
    return len([x for x in rooms.values() if x.shortest_path_len > 999])

print("Largest number of doors required to reach a room: %d" % part_one(INPUT))
print("Rooms 1000+ away: %d" % part_two(INPUT))








