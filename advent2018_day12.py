from collections import defaultdict
import numpy as np

INPUT = open("advent2018_day12_input.txt", "r").read().split("\n")
ALTINPUT = "initial state: #..#.#..##......###...###;;...## => #;..#.. => #;.#... => #;.#.#. => #;.#.## => #;.##.. => #;.#### => #;#.#.# => #;#.### => #;##.#. => #;##.## => #;###.. => #;###.# => #;####. => #".split(";")


def parse_input(lines):
    initial_state = lines[0][15:]
    rules = {}
    for line in lines[2:]:
        rules[line[:5]] = line[9]

    return initial_state, rules


def get_slice(state, i):
    return ''.join([state[x] for x in xrange(i-2, i+3)])


def get_min_max_known(state):
    keys = state.keys()
    return min(keys), max(keys)


def trim_state(state):
    min_known, max_known = get_min_max_known(state)
    i = min_known
    while state[i] == '.':
        del state[i]
        i += 1
    i = max_known
    while state[i] == '.':
        del state[i]
        i -= 1


def state_string(state):
    return ''.join([state[x] for x in sorted(state.keys())])


def mutate(current_state, rules):
    new_state = current_state.copy()
    min_known, max_known = get_min_max_known(current_state)
    for i in xrange(min_known-5, max_known+6):
        slice = get_slice(current_state, i)
        if slice in rules.keys():
            new_state[i] = rules[slice]
        else:
            new_state[i] = '.'
    trim_state(new_state)
    return new_state


def part_one(initial_state, rules):
    current_state = defaultdict(lambda: '.')
    for i in xrange(0, len(initial_state)):
        current_state[i] = initial_state[i]

    for i in xrange(1, 21):
        current_state = mutate(current_state, rules)

    full_pots = [key for key, value in current_state.iteritems() if value == '#']
    return sum(full_pots)


def part_two(initial_state, rules):
    current_state = defaultdict(lambda: '.')
    for i in xrange(0, len(initial_state)):
        current_state[i] = initial_state[i]

    for i in xrange(26000):
        current_state = mutate(current_state, rules)

    # At this point, I noticed that the mutation had settled into a steady predictable pattern.
    # That is to say, every thousand iterations produced the exact same plant positions, incremented by a thousand.
    # Thus, I can find the "base" positions, then add the offset necessary to bring them to the 50 billionth iteration.
    full_pots_at_26k = np.array([key for key, value in current_state.iteritems() if value == '#'])
    base_state = np.add(full_pots_at_26k, -26000)
    full_pots_at_50bil = np.add(base_state, 50000000000)
    return full_pots_at_50bil.sum()

initial_state, rules = parse_input(INPUT)

print("Full pots after 20 iterations: %d" % part_one(initial_state, rules))
print("Full pots after 50,000,000,000 iterations: %d" % part_two(initial_state, rules))
