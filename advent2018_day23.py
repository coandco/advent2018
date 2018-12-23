from collections import namedtuple, defaultdict
import re
INPUT = open("advent2018_day23_input.txt", "r").read().split("\n")

ALTINPUT = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".split("\n")

ALTINPUT_2 = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".split("\n")

REGEX = re.compile(r'pos=<(?P<posx>[^,]*),(?P<posy>[^,]*),(?P<posz>[^>]*)>, r=*(?P<radius>[0-9]*)')

Coord = namedtuple('Coord', ['x', 'y', 'z'])
Bot = namedtuple('Bot', ['pos', 'radius', 'origin_distance'])


def parse_input(lines):
    bots = {}
    for line in lines:
        match = REGEX.match(line)
        assert(match is not None)
        parts = match.groupdict()
        coord = Coord(x=int(parts['posx']), y=int(parts['posy']), z=int(parts['posz']))
        bot = Bot(pos=coord, radius=int(parts['radius']), origin_distance=abs(coord.x)+abs(coord.y)+abs(coord.z))
        assert coord not in bots.keys()
        bots[coord] = bot
    return bots


def get_distance(coord_one, coord_two):
    x_distance = abs(coord_two.x - coord_one.x)
    y_distance = abs(coord_two.y - coord_one.y)
    z_distance = abs(coord_two.z - coord_one.z)
    return x_distance + y_distance + z_distance


def ranges_overlap(bot_one, bot_two):
    distance = get_distance(bot_one.pos, bot_two.pos)
    return distance < (bot_one.radius + bot_two.radius)


def build_overlap_dict(bots):
    overlap_dict = defaultdict(set)
    for bot in bots.values():
        for other_bot in bots.values():
            # Don't recheck if you already know you're in range
            if other_bot.pos in overlap_dict[bot.pos]:
                continue
            if ranges_overlap(bot, other_bot):
                overlap_dict[bot.pos].add(other_bot.pos)
                overlap_dict[other_bot.pos].add(bot.pos)
    return overlap_dict


def prune_bots(bots, overlap_dict):
    OverlapResult = namedtuple('OverlapResult', ['pos', 'olist'])
    num_overlaps = sorted([OverlapResult(k, v) for k, v in overlap_dict.iteritems()],
                          key=lambda x: len(x.olist), reverse=True)
    while len(num_overlaps[0].olist) > len(num_overlaps[-1].olist):
        least_pos, least_olist = num_overlaps[-1]
        for drop_pos in least_olist:
            if drop_pos != least_pos:
                overlap_dict[drop_pos].remove(least_pos)
        del overlap_dict[least_pos]
        num_overlaps = sorted([OverlapResult(k, v) for k, v in overlap_dict.iteritems()],
                              key=lambda x: len(x.olist), reverse=True)

    random_overlap = overlap_dict.itervalues().next()
    for olist in overlap_dict.values():
        if random_overlap != olist:
            raise Exception("All bots have the same number of overlaps, but the sets are not equal")

    return [bots[x] for x in overlap_dict.keys()]


# Naive and hopelessly inefficient method.  Kept around for posterity.
def trace_sphere(range_map, bot):
    for i in xrange(bot.pos.x-bot.radius, bot.pos.x+bot.radius+1):
        start_point = Coord(x=i, y=bot.pos.y, z=bot.pos.z)
        cur_point = start_point
        prev_point = cur_point
        while get_distance(bot.pos, cur_point) <= bot.radius:
            prev_point = cur_point
            cur_point = Coord(x=cur_point.x, y=cur_point.y + 1, z=cur_point.z)
        slice_max = prev_point.y
        for j in xrange(start_point.y-slice_max, start_point.y+slice_max+1):
            # Go right until you're no longer within the radius
            for k in xrange(start_point.z+1, start_point.z+slice_max+1):
                cur_point = Coord(x=i, y=j, z=k)
                if get_distance(bot.pos, cur_point) <= bot.radius:
                    range_map[cur_point] += 1
                else:
                    break
            for k in xrange(start_point.z, start_point.z-slice_max-1, -1):
                cur_point = Coord(x=i, y=j, z=k)
                if get_distance(bot.pos, cur_point) <= bot.radius:
                    range_map[cur_point] += 1
                else:
                    break


def part_one(input):
    bots = parse_input(input)
    largest_bot = sorted(bots.values(), key=lambda x: x.radius, reverse=True)[0]
    bots_in_range = []
    for bot in bots.values():
        distance = get_distance(largest_bot.pos, bot.pos)
        if distance <= largest_bot.radius:
            bots_in_range.append(bot)

    return largest_bot, len(bots_in_range)


def part_two(input):
    bots = parse_input(input)
    overlap_dict = build_overlap_dict(bots)
    # Prune the bot list to only bots that overlapping ranges with every other bot in the set
    max_distance_surface_bot = max(prune_bots(bots, overlap_dict), key=lambda x: x.origin_distance-x.radius)
    guess = max_distance_surface_bot.origin_distance - max_distance_surface_bot.radius
    return guess


largest_range_bot, num_in_range = part_one(INPUT)
print("Bot with the largest range has coord %s and range %d" % (largest_range_bot.pos, largest_range_bot.radius))
print("Number of bots in range: %d" % num_in_range)

print("Guess for part two: %d" % part_two(INPUT))
