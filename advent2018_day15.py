from collections import namedtuple
from string import maketrans
import numpy as np

UNMAPPED = -1
WALL = -2
ELF = -3
GOBLIN = -4
PRINT_DICT = {UNMAPPED: '. ',
              WALL: '# ',
              ELF: 'E ',
              GOBLIN: 'G '}
np.set_printoptions(threshold=np.nan, linewidth=200, formatter={'int': lambda x: PRINT_DICT[x] if x in PRINT_DICT.keys() else "%02d" % x})

INPUT = open("advent2018_day15_input.txt", "r").read().split("\n")

# Correct outcome: 47 * 590 = 27730
ALTINPUT = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".split("\n")[1:]

# Correct outcome: 37 * 982 = 36334
ALTINPUT_2 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""".split("\n")[1:]

# Correct outcome: 46 * 859 = 39514
ALTINPUT_3 = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""".split("\n")[1:]

# Correct outcome: 35 * 793 = 27755
ALTINPUT_4 = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""".split('\n')[1:]

# Correct outcome: 54 * 536 = 28944
ALTINPUT_5 = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""".split('\n')[1:]

# Correct outcome: 20 * 937 = 18740
ALTINPUT_6 = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""".split('\n')[1:]


Coord = namedtuple("Coord", ["y", "x"])


class Fighter(object):
    types = {'G': 'Goblin', 'E': 'Elf'}

    def __init__(self, type, position, elf_attack):
        self.type = type
        self.position = position
        self.hp = 200
        self.attack = elf_attack if self.type == 'E' else 3

    def __repr__(self):
        return "Fighter(%s, %r, hp=%d, atk=%d)" % (self.types[self.type], self.position, self.hp, self.attack)


def get_fighters(field, elf_attack=3):
    combatants_dict = {}
    for i, line in enumerate(field):
        for j, char in enumerate(line):
            if char in ('G', 'E'):
                location = Coord(y=i, x=j)
                combatants_dict[location] = Fighter(char, location, elf_attack=elf_attack)
    return combatants_dict


def sanitize_field(field):
    new_field = field[:]
    translation = maketrans('GE', '..')
    for i, line in enumerate(new_field):
        new_field[i] = line.translate(translation)
    return new_field


def get_initial_state(input, elf_attack=3):
    fighters = get_fighters(input, elf_attack=elf_attack)
    field = sanitize_field(input)
    np_field = np.array([[-2 if x == '#' else -1 for x in y] for y in field], dtype=np.int)
    return np_field, fighters


def get_sorted_fighters(fighter_dict):
    return sorted(fighter_dict.values(), key=lambda x: (x.position.y, x.position.x))


def get_fighters_of_type(fighter_dict, type):
    return [x for x in get_sorted_fighters(fighter_dict) if x.type == type]


def add_coords(coord_one, coord_two):
    return Coord(x=coord_one.x+coord_two.x, y=coord_one.y+coord_two.y)


def within_bounds(coord, shape):
    return coord.x > 0 and coord.y > 0 and coord.x < shape[1] and coord.y < shape[0]


def get_populated_field(np_field, fighter_dict):
    populated_field = np_field.copy()
    # We can't pass through fighters
    for position, fighter in fighter_dict.iteritems():
        if fighter.type == 'E':
            populated_field[position] = ELF
        elif fighter.type == 'G':
            populated_field[position] = GOBLIN
    return populated_field


def print_populated_field(np_field, fighter_dict):
    stringified_field = ("%s" % get_populated_field(np_field, fighter_dict)).split("\n")
    for fighter in get_sorted_fighters(fighter_dict):
        stringified_field[fighter.position.y] += " %s(%d)" % (fighter.type, fighter.hp)
    print("\n".join(stringified_field))


DIRECTIONS = [(Coord(x=-1, y=0)), Coord(x=0, y=-1), Coord(x=1, y=0), Coord(x=0, y=1)]


def get_heatmap(populated_field, coord):
    heatmap_field = populated_field.copy()

    # Basically, we want to make sure we're not trying to get the heatmap starting at a wall
    assert(heatmap_field[coord] != WALL)

    # This spot is zero steps from itself
    heatmap_field[coord] = 0

    for direction in DIRECTIONS:
        new_coord = add_coords(coord, direction)
        if within_bounds(new_coord, heatmap_field.shape) and heatmap_field[new_coord] > WALL:
            update_heatmap(heatmap_field, new_coord, [new_coord])

    return heatmap_field


def update_heatmap(heatmap_field, coord, chain):
    heatmap_field[coord] = len(chain)

    for direction in DIRECTIONS:
        new_coord = add_coords(coord, direction)
        new_value = heatmap_field[new_coord]
        newchain = chain[:]
        newchain.append(new_coord)
        newchain_len = len(newchain)
        if within_bounds(new_coord, heatmap_field.shape) and (new_value == -1 or (0 <= newchain_len < new_value)):
            update_heatmap(heatmap_field, new_coord, newchain)


def get_range_targets_for_fighter(populated_field, fighter, enemy_fighters):
    targets = []
    for enemy in enemy_fighters:
        for direction in DIRECTIONS:
            possible_target = add_coords(enemy.position, direction)
            if within_bounds(possible_target, populated_field.shape):
                if possible_target == fighter.position or populated_field[possible_target] == UNMAPPED:
                    targets.append(possible_target)
    return targets


def get_all_min(coord_list, value_list):
    if not coord_list:
        return coord_list

    min_value = min(value_list)
    return [x for i, x in enumerate(coord_list) if value_list[i] == min_value]


def get_best_min(target_list, value_list):
    # Step one: filter targets to only ones with calculated values (0 and above)
    target_list = [x for i, x in enumerate(target_list) if value_list[i] >= 0]
    value_list = [x for x in value_list if x >= 0]

    # Step two: get all minimum targets
    minimum_targets = get_all_min(target_list, value_list)

    # Step three: pick the best one in reading order, if any
    return sorted(minimum_targets)[0] if minimum_targets else None


def select_target(populated_field, fighter, enemy_fighters, heatmap=None):
    if heatmap is None:
        heatmap = get_heatmap(populated_field, fighter.position)
    all_targets = get_range_targets_for_fighter(populated_field, fighter, enemy_fighters)
    reachable_targets = [x for x in all_targets if heatmap[x] >= 0]
    reachable_values = [heatmap[x] for x in reachable_targets]
    return get_best_min(reachable_targets, reachable_values)


def adjacent_squares(coord):
    return [add_coords(coord, x) for x in DIRECTIONS]


def find_best_move(populated_field, fighter, target):
    target_heatmap = get_heatmap(populated_field, target)
    possible_moves = adjacent_squares(fighter.position)
    possible_move_values = [target_heatmap[x] for x in possible_moves]
    return get_best_min(possible_moves, possible_move_values)


def fighter_turn(np_field, fighter, fighter_dict):
    '''
    fighter_turn -- run a single fighter's logic for a turn
    :param np_field: the bare numpy grid this is taking place on
    :param fighter: the individual fighter whose turn we're running
    :param fighter_dict: the dictionary of all known fighters
    :return: finished, elf_killed
    '''
    elf_died = False
    opposite_type = {'E': 'G', 'G': 'E'}
    populated_field = get_populated_field(np_field, fighter_dict)

    # Step one: get list of enemy fighters
    enemy_fighters = get_fighters_of_type(fighter_dict, opposite_type[fighter.type])
    if not enemy_fighters:
        return True, False

    if fighter.hp <= 0:
        return False, False

    # Step two: select a place we want to be and move towards it, if applicable
    target = select_target(populated_field, fighter, enemy_fighters)
    if target and target != fighter.position:
        move_coord = find_best_move(populated_field, fighter, target)
        if move_coord:
            del fighter_dict[fighter.position]
            fighter.position = move_coord
            assert(fighter.position not in fighter_dict.keys())
            fighter_dict[fighter.position] = fighter

    # Step three: determine adjacent enemy fighter with fewest hit points and fight it
    adjacent_enemies = [x for x in adjacent_squares(fighter.position)
                        if x in fighter_dict.keys() and fighter_dict[x].type == opposite_type[fighter.type]]
    enemy_hitpoints = [fighter_dict[x].hp for x in adjacent_enemies]
    min_enemies = get_all_min(adjacent_enemies, enemy_hitpoints)
    if min_enemies:
        best_enemy = sorted(min_enemies)[0]
        fighter_dict[best_enemy].hp -= fighter.attack
        if fighter_dict[best_enemy].hp <= 0:
            if fighter_dict[best_enemy].type == 'E':
                elf_died = True
            del fighter_dict[best_enemy]

    return False, elf_died


def run_battle(np_field, fighter_dict, no_elf_losses = False, debug=False):
    if debug:
        print("Initially:")
        print_populated_field(np_field, fighter_dict)

    finished = False
    num_turns_completed = 0

    while True:
        # sorted([fighter_dict[x] for x in fighter_dict.keys()], key=lambda x: x.position)
        remaining_fighters = get_sorted_fighters(fighter_dict)
        for fighter in remaining_fighters:
            finished, elf_died = fighter_turn(np_field, fighter, fighter_dict)
            if elf_died and no_elf_losses:
                return False
            if finished:
                break
        if finished:
            break
        num_turns_completed += 1
        if num_turns_completed % 10 == 0:
            print("Calculated %d rounds" % num_turns_completed)
        if debug:
            print("After %d round(s):" % num_turns_completed)
            print_populated_field(np_field, fighter_dict)

    print("Final field:")
    print_populated_field(np_field, fighter_dict)
    total_hitpoints = sum([x.hp for x in fighter_dict.values()])
    final_score = num_turns_completed * total_hitpoints
    print("Final score: %d*%d(%d)" % (num_turns_completed, total_hitpoints, final_score))
    return num_turns_completed, total_hitpoints, final_score


np_field, fighters = get_initial_state(INPUT, elf_attack=3)
num_turns_completed, total_hitpoints, final_score = run_battle(np_field, fighters, debug=False)
print("Part one result: %d*%d(%d)" % (num_turns_completed, total_hitpoints, final_score))

elf_attack = 15
while True:
    np_field, fighters = get_initial_state(INPUT, elf_attack=elf_attack)
    result = run_battle(np_field, fighters, debug=False, no_elf_losses=True)
    if result:
        num_turns_completed, total_hitpoints, final_score = result
        print("Part two result, with elf attack of %d: %d*%d(%d)" % (elf_attack, num_turns_completed,
                                                                     total_hitpoints, final_score))
        break
    else:
        print("Failed with elf attack of %d" % elf_attack)
        elf_attack += 1