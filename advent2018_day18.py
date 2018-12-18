import numpy as np
from collections import namedtuple
INPUT = open("advent2018_day18_input.txt", "r").read().split("\n")

OPEN_GROUND = 0
TREE = 1
LUMBERYARD = 2

PRINT_DICT = {OPEN_GROUND: '.',
              TREE: '|',
              LUMBERYARD: '#'}
READ_DICT = {v: k for k, v in PRINT_DICT.iteritems()}
np.set_printoptions(threshold=np.nan, linewidth=2000, formatter={'int': lambda x: PRINT_DICT[x] if x in PRINT_DICT.keys() else "%d" % x})


Coord = namedtuple('Coord', ['y', 'x'])


def make_field(input):
    width = len(input[0])
    height = len(input)
    np_field = np.fromfunction(shape=(height, width), dtype=np.int, function=np.vectorize(lambda y, x: READ_DICT[input[y][x]]))
    return np_field


def compute_next_step(y, x):
    coord = Coord(x=x, y=y)
    max_y, max_x = np_field.shape
    slice = np_field[max(coord.y-1, 0):min(coord.y+2, max_y+1), max(coord.x-1, 0):min(coord.x+2, max_x+1)]
    if np_field[coord] == OPEN_GROUND:
        num_trees = (slice == TREE).sum()
        return TREE if num_trees >= 3 else OPEN_GROUND
    elif np_field[coord] == TREE:
        num_lumberyards = (slice == LUMBERYARD).sum()
        return LUMBERYARD if num_lumberyards >= 3 else TREE
    elif np_field[coord] == LUMBERYARD:
        num_trees = (slice == TREE).sum()
        # Don't count the lumberyard in the middle
        num_lumberyards = (slice == LUMBERYARD).sum() - 1
        return LUMBERYARD if (num_trees >= 1 and num_lumberyards >= 1) else OPEN_GROUND


ALTINPUT = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".split("\n")[1:]


np_field = make_field(INPUT)
old_field = np_field.copy()
for i in xrange(1, 1000000000):
    np_field = np.fromfunction(np.vectorize(compute_next_step), np_field.shape, dtype=int)
    if i == 10:
        num_trees = (np_field == TREE).sum()
        num_lumberyards = (np_field == LUMBERYARD).sum()
        print("After 10 minutes, Trees: %d Lumberyards: %d Total value: %d" %
              (num_trees, num_lumberyards, num_trees * num_lumberyards))

    # Dumped the value each iteration and discovered it repeated every 28 cycles once it settles
    if i % 28 == (1000000000 % 28):
        if np.array_equal(np_field, old_field):
            num_trees = (np_field == TREE).sum()
            num_lumberyards = (np_field == LUMBERYARD).sum()
            print("After 1000000000 minutes, Trees: %d Lumberyards: %d Total value: %d" %
                  (num_trees, num_lumberyards, num_trees * num_lumberyards))
            break
        else:
            old_field = np_field.copy()
