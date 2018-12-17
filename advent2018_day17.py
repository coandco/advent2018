import numpy as np
from collections import namedtuple
INPUT = open("advent2018_day17_input.txt", "r").read().split("\n")

UNMAPPED = 0
WALL = 1
FALLING_WATER = -1
RESTING_WATER = 2
PRINT_DICT = {UNMAPPED: '.',
              WALL: '#',
              FALLING_WATER: '|',
              RESTING_WATER: '~'}
np.set_printoptions(threshold=np.nan, linewidth=2000, formatter={'int': lambda x: PRINT_DICT[x] if x in PRINT_DICT.keys() else "%d" % x})

ALTINPUT = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".split("\n")


Coord = namedtuple('Coord', ['y', 'x'])


def parse_line(line):
    point, line_range = line.split(',')
    point_axis, point_value = point.split("=")
    range_axis, range_value = line_range[1:].split("=")
    range_start, range_end = range_value.split("..")
    point_list = []
    for i in xrange(int(range_start), int(range_end)+1):
        if range_axis == 'x':
            point_list.append(Coord(x=i, y=int(point_value)))
        elif range_axis == 'y':
            point_list.append(Coord(x=int(point_value), y=i))
        else:
            raise Exception("Unknown axis encountered: %s" % range_axis)
    return point_list


def in_range(coordinate, shape):
    return (0 < coordinate.y < shape[0]) and (0 < coordinate.x < shape[1])

def down(coordinate):
    return Coord(x=coordinate.x, y=coordinate.y+1)

def up(coordinate):
    return Coord(x=coordinate.x, y=coordinate.y-1)

def left(coordinate):
    return Coord(x=coordinate.x-1, y=coordinate.y)

def right(coordinate):
    return Coord(x=coordinate.x+1, y=coordinate.y)


def water_fall(np_field, starting_point):
    current_position = starting_point
    while True:
        if not in_range(down(current_position), np_field.shape):
            np_field[current_position] = FALLING_WATER
            return None
        elif np_field[down(current_position)] in (WALL, RESTING_WATER):
            return current_position
        else:
            np_field[current_position] = FALLING_WATER
            current_position = down(current_position)


Bound = namedtuple('Bound', ['coord', 'is_wall'])


class Node(object):
    def __init__(self, location, parent=None):
        self.location = location
        self.left = None
        self.right = None
        self.parent = parent
        self.finished = False

    def __repr__(self):
        return "Node(y=%d, x=%d, finished=%s" % (self.location.y, self.location.x, self.finished)

    def __cmp__(self, other):
        if other is None:
            return False
        else:
            return self.location == other.location


def get_leaves(node, known_nodes=None):
    if known_nodes is None:
        known_nodes = set()
    known_nodes.add(node.location)

    if node.left is None and node.right is None and not node.finished:
        return [node], known_nodes

    if node.left and node.left.location not in known_nodes:
        left_leaves, known_nodes = get_leaves(node.left, known_nodes)
    else:
        left_leaves = []

    if node.right and node.right.location not in known_nodes:
        right_leaves, known_nodes = get_leaves(node.right, known_nodes)
    else:
        right_leaves = []

    return (left_leaves + right_leaves), known_nodes


def remove_node(node):
    if node.parent.left is node:
        node.parent.left = None
        node.parent.finished = False
    if node.parent.right is node:
        node.parent.right = None
        node.parent.finished = False


def water_spread(np_field, node):
    starting_point = water_fall(np_field, node.location)
    if not starting_point:
        node.finished = True
        return

    if starting_point.y == node.location.y:
        remove_node(node)
    current_position = starting_point

    # Start by spreading left
    while True:
        if np_field[left(current_position)] in (WALL, RESTING_WATER):
            left_bound = Bound(coord=current_position, is_wall=True)
            break
        elif np_field[down(left(current_position))] in (WALL, RESTING_WATER):
            current_position = left(current_position)
        else:
            left_bound = Bound(coord=left(current_position), is_wall=False)
            break


    # Then spread right
    current_position = starting_point
    while True:
        if np_field[right(current_position)] in (WALL, RESTING_WATER):
            right_bound = Bound(coord=current_position, is_wall=True)
            break
        elif np_field[down(right(current_position))] in (WALL, RESTING_WATER):
            current_position = right(current_position)
        else:
            right_bound = Bound(coord=right(current_position), is_wall=False)
            break

    # Fill in
    if left_bound.is_wall and right_bound.is_wall:
        np_field[starting_point.y, left_bound.coord.x:right_bound.coord.x + 1] = RESTING_WATER
        return True
    else:
        np_field[starting_point.y, left_bound.coord.x:right_bound.coord.x + 1] = FALLING_WATER
        node.finished = True

        if not left_bound.is_wall:
            node.left = Node(left_bound.coord, parent=node)

        if not right_bound.is_wall:
            node.right = Node(right_bound.coord, parent=node)


def run_iteration(np_field, base_node):
    leaf_nodes, _ = get_leaves(base_node)
    if not leaf_nodes:
        return True
    else:
        for node in leaf_nodes:
            water_spread(np_field, node)
        return False



point_list = []
for line in INPUT:
    point_list.extend(parse_line(line))

y, x = zip(*point_list)
min_x = min(x)
print("Offset: %d" % (min_x - 1))
max_x = max(x)
min_y = min(y)
max_y = max(y)

np_field = np.zeros(shape=(max_y+1, max_x+2), dtype=np.int)
for point in point_list:
    np_field[point] = WALL


starting_point = Node(Coord(x=500, y=0))
complete = False
iteration = 0
while not complete:
    iteration += 1
    complete = run_iteration(np_field, starting_point)

print(np_field[:, min_x - 1:])
print(np.count_nonzero(np_field[min_y:,] == RESTING_WATER) + np.count_nonzero(np_field[min_y:,] == FALLING_WATER))
print(np.count_nonzero(np_field[min_y:,] == RESTING_WATER))





