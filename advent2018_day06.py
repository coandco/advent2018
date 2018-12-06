import numpy
from collections import namedtuple
Coordinate = namedtuple('Coordinate', 'x y')


def get_distance(first_loc, second_loc):
    distance_x = first_loc.x - second_loc.x
    distance_y = first_loc.y - second_loc.y
    return abs(distance_x) + abs(distance_y)


def closest_point(location, list_of_points):
    distances = [get_distance(location, x) for x in list_of_points]
    smallest_distance = min(distances)
    smallest_distances = []
    for i, distance in enumerate(distances):
        if distance == smallest_distance:
            smallest_distances.append(i)

    if len(smallest_distances) == 1:
        return smallest_distances[0]
    else:
        return -1


def within_range(location, list_of_points, range):
    return int(sum([get_distance(location, x) for x in list_of_points]) < range)


INPUT = open("advent2018_day06_input.txt", "r").read().split("\n")
ALTINPUT = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".split("\n")



INPUT_SHAPE = (380, 380)
PROCESSED_INPUT = [Coordinate(x=int(x.split(",")[0]), y=int(x.split(",")[1])) for x in INPUT]
RANGE = 10000

#INPUT_SHAPE = (10, 10)
#PROCESSED_INPUT = [Coordinate(x=int(x.split(",")[0]), y=int(x.split(",")[1])) for x in ALTINPUT]
#RANGE = 32

grid = numpy.full(INPUT_SHAPE, fill_value=-1, dtype=int)

infinite_points = set()

for i, item in numpy.ndenumerate(grid):
    # i is returned in format (y, x)
    coord = Coordinate(i[1], i[0])
    grid[coord.y, coord.x] = closest_point(coord, PROCESSED_INPUT)
    if coord.x == 0 or coord.y == 0 or coord.x == INPUT_SHAPE[1]-1 or coord.y == INPUT_SHAPE[0]-1:
        infinite_points.add(grid[coord.y, coord.x])

areas = {}
for i, item in enumerate(PROCESSED_INPUT):
    if i not in infinite_points:
        areas[i] = (grid == i).sum()

largest_area = max(areas, key=areas.get)
print("Max is index %d with area %d" % (largest_area, areas[largest_area]))

grid_two = numpy.zeros(INPUT_SHAPE, dtype=int)
for i, item in numpy.ndenumerate(grid):
    # i is returned in format (y, x)
    coord = Coordinate(i[1], i[0])
    grid_two[coord.y, coord.x] = within_range(coord, PROCESSED_INPUT, RANGE)

print("Size of area within range: %d" % grid_two.sum())