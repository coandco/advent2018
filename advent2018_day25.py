from collections import namedtuple
INPUT = open("advent2018_day25_input.txt", "r").read().split("\n")

ALTINPUT = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""".split("\n")

Coord = namedtuple('Coord', ['x', 'y', 'z', 't'])


def get_distance(coord_one, coord_two):
    x_distance = abs(coord_two.x - coord_one.x)
    y_distance = abs(coord_two.y - coord_one.y)
    z_distance = abs(coord_two.z - coord_one.z)
    t_distance = abs(coord_two.t - coord_one.t)
    return x_distance + y_distance + z_distance + t_distance


def parse_input(lines):
    point_list = []
    for line in lines:
        new_point = Coord(*[int(x) for x in line.split(",")])
        point_list.append(new_point)
    return point_list


def part_one(point_list):
    constellations = [[point_list[0]]]

    for point in point_list[1:]:
        homes = []
        for i, constellation in enumerate(constellations):
            for con_point in constellation:
                distance = get_distance(point, con_point)
                if distance <= 3:
                    homes.append(i)
                    break
        if homes:
            constellations[homes[0]].append(point)
            for merge_index in homes[1:]:
                constellations[homes[0]].extend(constellations[merge_index])
                constellations[merge_index] = None
            constellations = [x for x in constellations if x]
        else:
            constellations.append([point])
    return len(constellations)


point_list = parse_input(INPUT)
print("Number of constellations: %d" % part_one(point_list))
