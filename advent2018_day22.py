from collections import namedtuple
import numpy as np


# So, this was fun.  Not only do I have to set the recursion limit higher, but I can't run this code in Windows.
# If I try, Windows terminates the process with an "out of stack space" return code.
import sys
sys.setrecursionlimit(10000)

Coord = namedtuple('Coord', ['y', 'x'])
INPUT_DEPTH = 8103
INPUT_TARGET = Coord(x=9, y=758)

TEST_DEPTH = 510
TEST_TARGET = Coord(x=10, y=10)

ROCKY = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
CLIMBGEAR = 2

SWITCH_COST = 7

PRINT_DICT = {ROCKY: '.',
              WET: '=',
              NARROW: '|'}
np.set_printoptions(threshold=np.nan, linewidth=2000,
                    formatter={'int': lambda x: PRINT_DICT[x] if x in PRINT_DICT.keys() else "%d" % x,
                               'bool': lambda x: '#' if x else '.'})


def output_field(e_field):
    def _erosion_level(y, x):
        return e_field[y, x] % 3
    return _erosion_level


def calc_field(depth, target):
    # With my input, I need to have a buffer of 40 to support the optimal path
    e_field = np.zeros(shape=(target.y+40, target.x+40), dtype=np.int)
    erosion_mod = 20183

    # Init 0, 0
    e_field[0, 0] = depth % erosion_mod
    # Init the sides
    for i in xrange(1, e_field.shape[1]):
        e_field[0, i] = ((i * 16807) + depth) % erosion_mod
    for i in xrange(1, e_field.shape[0]):
        e_field[i, 0] = ((i * 48271) + depth) % erosion_mod

    # Progressively calculate values based on previous values
    for i in xrange(1, e_field.shape[0]):
        for j in xrange(1, e_field.shape[1]):
            if (i, j) == target:
                # Init the target location when we run across it
                e_field[i, j] = depth % erosion_mod
            else:
                e_field[i, j] = ((e_field[i-1, j] * e_field[i, j-1]) + depth) % erosion_mod

    return np.fromfunction(np.vectorize(output_field(e_field)), shape=e_field.shape, dtype=int)


def add_coords(coord_one, coord_two):
    return Coord(x=coord_one.x+coord_two.x, y=coord_one.y+coord_two.y)


def within_bounds(coord, shape):
    return coord.x >= 0 and coord.y >= 0 and coord.x < shape[1] and coord.y < shape[0]


DIRECTIONS = [(Coord(x=-1, y=0)), Coord(x=0, y=-1), Coord(x=1, y=0), Coord(x=0, y=1)]
HEATMAP_IMPASSABLE = -2
HEATMAP_UNEXPLORED = -1
HEATMAP_PRINT_DICT = {HEATMAP_IMPASSABLE: '#', HEATMAP_UNEXPLORED: '.'}


def update_heatmap(heatmap_field, coord, startvalue, touched_locations=None):
    if touched_locations is None:
        touched_locations = set()
    assert heatmap_field[coord] != HEATMAP_IMPASSABLE
    heatmap_field[coord] = startvalue
    touched_locations.add(coord)

    for direction in DIRECTIONS:
        new_coord = add_coords(coord, direction)
        new_value = startvalue + 1
        if within_bounds(new_coord, heatmap_field.shape):
            existing_value = heatmap_field[new_coord]
            if existing_value == HEATMAP_UNEXPLORED or (0 <= new_value < existing_value):
                touched_locations = update_heatmap(heatmap_field, new_coord, new_value, touched_locations)

    return touched_locations


def valid_adjacent(heatmap_field, coord):
    possibilities = set([add_coords(coord, x) for x in DIRECTIONS])
    for loc in list(possibilities):
        if not within_bounds(loc, heatmap_field.shape):
            possibilities.remove(loc)
        elif heatmap_field[loc] == HEATMAP_IMPASSABLE:
            possibilities.remove(loc)
    return possibilities


def update_heatmap_v2(heatmap_field, coord_set, new_value):
    touched_locations = set()
    next_locations = set()
    for coord in coord_set:
        if within_bounds(coord, heatmap_field.shape):
            existing_value = heatmap_field[coord]
            if existing_value == HEATMAP_UNEXPLORED or (0 <= new_value < existing_value):
                heatmap_field[coord] = new_value
                touched_locations.add(coord)
                next_locations.update(valid_adjacent(heatmap_field, coord))
    next_locations -= coord_set
    if next_locations:
        touched_locations.update(update_heatmap_v2(heatmap_field, next_locations, new_value+1))
    return touched_locations


def print_heatmap(heatmap):
    # 'with np.printoptions' requires numpy 1.15.0 or above
    with np.printoptions(threshold=np.nan, linewidth=2000,
                         formatter={'int': lambda x: "%4s" % HEATMAP_PRINT_DICT[x] if x in HEATMAP_PRINT_DICT.keys() else "%4d" % x}):
        print(heatmap)


def switch_tool(terrain_type, active_tool):
    possible_tools = {0, 1, 2}
    possible_tools.remove(terrain_type)
    possible_tools.remove(active_tool)
    return possible_tools.pop()


def run_iteration(terrain, heatmaps, active_sites):
    # Broadly speaking: for each location in active sites, switch tools,
    # update new-tool heatmap from that location, make note of new sites seen and return that
    new_sites = [set(), set(), set()]
    for tool in (NEITHER, TORCH, CLIMBGEAR):
        for site in active_sites[tool]:
            new_tool = switch_tool(terrain[site], tool)
            if heatmaps[new_tool][site] == -1 or (0 < (heatmaps[tool][site]+SWITCH_COST) < heatmaps[new_tool][site]):
                new_sites[new_tool].update(update_heatmap_v2(heatmaps[new_tool], {site}, heatmaps[tool][site]+SWITCH_COST))
    return new_sites


DEPTH = INPUT_DEPTH
TARGET = INPUT_TARGET
generated_field = calc_field(DEPTH, TARGET)
neither_field = (((generated_field == NEITHER)*-1)-1)
torch_field = (((generated_field == TORCH)*-1)-1)
climbgear_field = (((generated_field == CLIMBGEAR)*-1)-1)

heatmaps = [neither_field, torch_field, climbgear_field]
active_sites = [set(), update_heatmap(heatmaps[TORCH], Coord(x=0, y=0), 0), set()]

while sum([len(x) for x in active_sites]) > 0:
    active_sites = run_iteration(generated_field, heatmaps, active_sites)

print("Danger level of generated field: %d" % generated_field[0:TARGET.y+1, 0:TARGET.x+1].sum())
print("Shortest path to target: %d" % min(heatmaps[TORCH][TARGET], heatmaps[CLIMBGEAR][TARGET]+SWITCH_COST))
