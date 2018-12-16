EXAMPLES, PROGRAM = open("advent2018_day16_input.txt", "r").read().split("\n\n\n")
EXAMPLES = EXAMPLES.split("\n\n")
PROGRAM = PROGRAM.split("\n")[1:-1]

ALTINPUT = ["""Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""]

class RegisterOutOfBoundsError(Exception):
    pass


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


def try_store(value, register_number, registers):
    try:
        registers[register_number] = value
    except IndexError:
        raise RegisterOutOfBoundsError


def try_load(register_number, registers):
    try:
        return registers[register_number]
    except IndexError:
        raise RegisterOutOfBoundsError


def op_r(opcodes, registers, lambda_func):
    new_registers = registers[:]
    value_a = try_load(opcodes[1], registers)
    value_b = try_load(opcodes[2], registers)
    try_store(lambda_func(value_a, value_b), opcodes[3], new_registers)
    return new_registers

def op_i(opcodes, registers, lambda_func):
    new_registers = registers[:]
    value_a = try_load(opcodes[1], registers)
    value_b = opcodes[2]
    try_store(lambda_func(value_a, value_b), opcodes[3], new_registers)
    return new_registers


def cmp_ir(opcodes, registers, lambda_func):
    new_registers = registers[:]
    value_a = opcodes[1]
    value_b = try_load(opcodes[2], registers)
    try_store(lambda_func(value_a, value_b), opcodes[3], new_registers)
    return new_registers


def cmp_ri(opcodes, registers, lambda_func):
    new_registers = registers[:]
    value_a = try_load(opcodes[1], registers)
    value_b = opcodes[2]
    try_store(lambda_func(value_a, value_b), opcodes[3], new_registers)
    return new_registers


def cmp_rr(opcodes, registers, lambda_func):
    new_registers = registers[:]
    value_a = try_load(opcodes[1], registers)
    value_b = try_load(opcodes[2], registers)
    try_store(lambda_func(value_a, value_b), opcodes[3], new_registers)
    return new_registers


def addr(opcodes, registers):
    return op_r(opcodes, registers, lambda_func=lambda x,y: x+y)


def addi(opcodes, registers):
    return op_i(opcodes, registers, lambda_func=lambda x,y: x+y)


def mulr(opcodes, registers):
    return op_r(opcodes, registers, lambda_func=lambda x,y: x*y)


def muli(opcodes, registers):
    return op_i(opcodes, registers, lambda_func=lambda x,y: x*y)


def banr(opcodes, registers):
    return op_r(opcodes, registers, lambda_func=lambda x,y: x&y)


def bani(opcodes, registers):
    return op_i(opcodes, registers, lambda_func=lambda x,y: x&y)


def borr(opcodes, registers):
    return op_r(opcodes, registers, lambda_func=lambda x,y: x|y)


def bori(opcodes, registers):
    return op_i(opcodes, registers, lambda_func=lambda x,y: x|y)


def setr(opcodes, registers):
    new_registers = registers[:]
    value_a = try_load(opcodes[1], registers)
    try_store(value_a, opcodes[3], new_registers)
    return new_registers


def seti(opcodes, registers):
    new_registers = registers[:]
    try_store(opcodes[1], opcodes[3], new_registers)
    return new_registers


def gtir(opcodes, registers):
    return cmp_ir(opcodes, registers, lambda_func=lambda x,y: 1 if x > y else 0)


def gtri(opcodes, registers):
    return cmp_ri(opcodes, registers, lambda_func=lambda x,y: 1 if x > y else 0)


def gtrr(opcodes, registers):
    return cmp_rr(opcodes, registers, lambda_func=lambda x,y: 1 if x > y else 0)


def eqir(opcodes, registers):
    return cmp_ir(opcodes, registers, lambda_func=lambda x,y: 1 if x == y else 0)


def eqir(opcodes, registers):
    return cmp_ir(opcodes, registers, lambda_func=lambda x,y: 1 if x == y else 0)


def eqri(opcodes, registers):
    return cmp_ri(opcodes, registers, lambda_func=lambda x,y: 1 if x == y else 0)


def eqrr(opcodes, registers):
    return cmp_rr(opcodes, registers, lambda_func=lambda x,y: 1 if x == y else 0)


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


OPCODE_DICT = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


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
