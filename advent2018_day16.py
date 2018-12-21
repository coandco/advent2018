from assembler import OPCODE_DICT, RegisterOutOfBoundsError
EXAMPLES, PROGRAM = open("advent2018_day16_input.txt", "r").read().split("\n\n\n")
EXAMPLES = EXAMPLES.split("\n\n")
PROGRAM = PROGRAM.split("\n")[1:-1]

ALTINPUT = ["""Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""]

class Example(object):
    def __init__(self, before, opcodes, after):
        self.before = before
        self.opcodes = opcodes
        self.after = after


def create_example(text_in):
    before, opcodes, after = text_in.split("\n")
    before = [int(x) for x in before[9:-1].split(",")]
    opcodes = [int(x) for x in opcodes.split(" ")]
    after = [int(x) for x in after[9:-1].split(",")]
    return Example(before, opcodes, after)


PROCESSED_EXAMPLES = [create_example(x) for x in EXAMPLES]


def remove_item_from_possibilities(opcode, possibilities):
    new_possibilities = []
    for possibility in possibilities:
        new_list = [x for x in possibility[1] if x != opcode]
        if new_list:
            new_possibilities.append((possibility[0], new_list))
    return new_possibilities


def build_opcode_dict(possibilities):
    known_opcodes = {}
    while True:
        known = [x for x in possibilities if len(x[1]) == 1]
        if known:
            number, opcode = known[0][0], known[0][1][0]
            known_opcodes[number] = opcode
            possibilities = remove_item_from_possibilities(opcode, possibilities)
            if len(possibilities) == 0:
                break
        else:
            break
    return known_opcodes


def part_one(examples):
    three_or_more = 0
    possibility_space = []
    for example in examples:
        possible_opcodes = []

        for opcode, opcode_func in OPCODE_DICT.iteritems():
            try:
                result = opcode_func(example.opcodes, example.before)
            except RegisterOutOfBoundsError:
                continue
            if result == example.after:
                possible_opcodes.append(opcode)
        # print("%r could be opcodes %r" % (example.opcodes, possible_opcodes))
        if len(possible_opcodes) >= 3:
            three_or_more += 1
        possibility_space.append((example.opcodes[0], possible_opcodes))
    return three_or_more, possibility_space


def part_two(possibility_space, program):
    known_opcodes = build_opcode_dict(possibility_space)
    actual_opcode_dict = {x: OPCODE_DICT[known_opcodes[x]] for x in known_opcodes.keys()}

    registers = [0, 0, 0, 0]
    for line in program:
        opcodes = [int(x) for x in line.split(" ")]
        registers = actual_opcode_dict[opcodes[0]](opcodes, registers)
    return registers


three_or_more, possibility_space = part_one(PROCESSED_EXAMPLES)
print("Number of examples with three or more possibilities: %d" % three_or_more)

final_registers = part_two(possibility_space, PROGRAM)
print("Final registers: %r" % final_registers)
