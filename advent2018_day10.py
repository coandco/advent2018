import re
import numpy as np

np.set_printoptions(linewidth=130, formatter={'bool': lambda x: '#' if x else ' '})

INPUT = open("advent2018_day10_input.txt", "r").read().split("\n")
ALTINPUT = "position=< 9,  1> velocity=< 0,  2>;position=< 7,  0> velocity=<-1,  0>;position=< 3, -2> velocity=<-1,  1>;position=< 6, 10> velocity=<-2, -1>;position=< 2, -4> velocity=< 2,  2>;position=<-6, 10> velocity=< 2, -2>;position=< 1,  8> velocity=< 1, -1>;position=< 1,  7> velocity=< 1,  0>;position=<-3, 11> velocity=< 1, -2>;position=< 7,  6> velocity=<-1, -1>;position=<-2,  3> velocity=< 1,  0>;position=<-4,  3> velocity=< 2,  0>;position=<10, -3> velocity=<-1,  1>;position=< 5, 11> velocity=< 1, -2>;position=< 4,  7> velocity=< 0, -1>;position=< 8, -2> velocity=< 0,  1>;position=<15,  0> velocity=<-2,  0>;position=< 1,  6> velocity=< 1,  0>;position=< 8,  9> velocity=< 0, -1>;position=< 3,  3> velocity=<-1,  1>;position=< 0,  5> velocity=< 0, -1>;position=<-2,  2> velocity=< 2,  0>;position=< 5, -2> velocity=< 1,  2>;position=< 1,  4> velocity=< 2,  1>;position=<-2,  7> velocity=< 2, -2>;position=< 3,  6> velocity=<-1, -1>;position=< 5,  0> velocity=< 1,  0>;position=<-6,  0> velocity=< 2,  0>;position=< 5,  9> velocity=< 1, -2>;position=<14,  7> velocity=<-2,  0>;position=<-3,  6> velocity=< 2, -1>".split(";")

REGEX = re.compile(r'position=< *(?P<posx>[^,]*), *(?P<posy>[^>]*)> velocity=< *(?P<velx>[^,]*), *(?P<vely>[^>]*)')


def read_line(line):
    match = REGEX.match(line)
    assert(match is not None)
    parts = match.groupdict()
    return (int(parts['posx']), int(parts['posy'])), (int(parts['velx']), int(parts['vely']))


def update_positions(positions, velocities):
    return np.add(positions, velocities)


def get_scatter_size(positions):
    xmax, ymax = np.amax(positions, axis=0)
    xmin, ymin = np.amin(positions, axis=0)
    return xmax-xmin, ymax-ymin


def printable_array(positions):
    min_x, min_y = np.amin(positions, axis=0)
    max_x, max_y = np.amax(positions, axis=0)
    shaved_array = np.add(positions, (-min_x, -min_y))
    new_array = np.zeros([max_y-min_y+1, max_x-min_x+1], dtype=np.bool)
    for x, y in shaved_array:
        new_array[y, x] = True
    return new_array


PARSED_INPUT = [read_line(x) for x in INPUT]
PARSED_POSITIONS, PARSED_VELOCITIES = zip(*PARSED_INPUT)

generation = 1
current_positions = PARSED_POSITIONS
x_size, y_size = get_scatter_size(current_positions)
while True:
    previous_positions = current_positions
    current_positions = np.add(current_positions, PARSED_VELOCITIES)
    old_x_size, old_y_size = x_size, y_size
    x_size, y_size = get_scatter_size(current_positions)
    if y_size < 100 and old_x_size*old_y_size <= x_size*y_size:
        print("For generation %d, size is %dx%d" % (generation-1, old_x_size, old_y_size))
        output_array = printable_array(previous_positions)
        print(output_array)
        break
    generation += 1

