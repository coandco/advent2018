import string

INPUT = open("advent2018_day21_input.txt", "r").read().split("\n")


def parse_input(lines):
    ip = int(lines[0].split(" ")[-1])
    instructions = []
    for line in lines[1:]:
        opcodes = [int(x) if x[0] not in string.ascii_letters else x for x in line.split(" ")]
        instructions.append(opcodes)
    return ip, instructions


class RegisterOutOfBoundsError(Exception):
    pass


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


def eqri(opcodes, registers):
    return cmp_ri(opcodes, registers, lambda_func=lambda x,y: 1 if x == y else 0)


def eqrr(opcodes, registers):
    return cmp_rr(opcodes, registers, lambda_func=lambda x,y: 1 if x == y else 0)


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


INPUT_EXPLAINED = """00: seti 123 0 4      # r[4] = 123
01: bani 4 456 4      # r[4] &= 456
02: eqri 4 72 4       # r[4] = 1 if r[4] == 72 else 0
03: addr 4 1 1        # Jump to instruction 5 if r[4] == 72
04: seti 0 0 1        # Jump to instruction 1
05: seti 0 4 4        # r[4] = 0
06: bori 4 65536 3    # r[3] = r[4] | 65536(0b1 00000000 00000000)
07: seti 12670166 8 4 # r[4] = 12670166 (0b11000001 01010100 11010110)
08: bani 3 255 2      # r[2] = r[3] & 255 (0b11111111)
09: addr 4 2 4        # r[4] += r[2]
10: bani 4 16777215 4 # r[4] &= 16777215 (0b11111111 11111111 11111111)
11: muli 4 65899 4    # r[4] *= 65899 (0b1 00000001 01101011)
12: bani 4 16777215 4 # r[4] &= 16777215 (0b11111111 11111111 11111111)
13: gtir 256 3 2      # r[2] = 1 if 256 > r[3] else 0
14: addr 2 1 1        # Jump to instruction 16 if 256 > r[3]
15: addi 1 1 1        # Jump to instruction 17
16: seti 27 6 1       # Jump to instruction 28
17: seti 0 0 2        # r[2] = 0
18: addi 2 1 5        # r[5] = r[2] + 1
19: muli 5 256 5      # r[5] *= 256
20: gtrr 5 3 5        # r[5] = 1 if r[5] > r[3] else 0
21: addr 5 1 1        # Jump to instruction 23 if r[5] was > r[3]  
22: addi 1 1 1        # Jump to instruction 24
23: seti 25 6 1       # Jump to instruction 26
24: addi 2 1 2        # r[2] += 1
25: seti 17 8 1       # Jump to instruction 18
26: setr 2 5 3        # r[3] = r[2]
27: seti 7 2 1        # Jump to instruction 8
28: eqrr 4 0 2        # r[2] = 1 if r[4] == r[0] else 0
29: addr 2 1 1        # End program if r[4] == r[0]
30: seti 5 8 1        # Jump to instruction 6""".split("\n")


def opcode_str(opcode):
    return "%s %d %d %d" % tuple(opcode)


def binary_pp(number, ):
    byte_array = []
    while number > 0:
        low_byte = number & 255
        byte_array.append(low_byte)
        number = number >> 8
    if not byte_array:
        byte_array = [0]
    return "0b%s" % " ".join(["{0:08b}".format(x) for x in reversed(byte_array)])


def registers_str(reg):
    return "[%d, %d, %s, %s, %s, %s]" % (reg[0], reg[1], binary_pp(reg[2]),
                                         binary_pp(reg[3]), binary_pp(reg[4]), binary_pp(reg[5]))


def part_one(lines):
    ip_reg_num, instructions = parse_input(lines)

    registers = [0, 0, 0, 0, 0, 0]
    pc = registers[ip_reg_num]
    iteration = 0
    while 0 <= pc < len(instructions):
        iteration += 1
        registers[ip_reg_num] = pc
        opcode = instructions[pc]

        # Line 28 is where it compares the value it's generated to the register you're passing in.
        # Therefore, to find the input that will cause it to quit the fastest, return the first value it generates.
        if pc == 28:
            break

        registers = OPCODE_DICT[opcode[0]](opcode, registers)

        pc = registers[ip_reg_num]
        pc += 1
    return registers[4]


def part_two(lines):
    ip_reg_num, instructions = parse_input(lines)

    registers = [0, 0, 0, 0, 0, 0, 0]
    pc = registers[ip_reg_num]
    iteration = 0
    seen_values = set()
    previous_value = None
    while 0 <= pc < len(instructions):
        iteration += 1
        registers[ip_reg_num] = pc
        opcode = instructions[pc]

        # To find the minimum input that will result in the longest runtime, we want to find
        # the last value it generates before repeating itself.
        if pc == 28:
            if registers[4] in seen_values:
                return previous_value
            else:
                seen_values.add(registers[4])
                previous_value = registers[4]

        registers = OPCODE_DICT[opcode[0]](opcode, registers)

        # This short-circuits the pointless "increment by one" logic and skips directly
        # to the value that allows it to continue
        if pc == 17:
            registers[2] = registers[3] >> 8

        pc = registers[ip_reg_num]
        pc += 1
    return registers


print("First break value: %d" % part_one(INPUT))
print("Last non-repeat value: %d" % part_two(INPUT))