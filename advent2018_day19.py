import string
from functools import reduce
from assembler import OPCODE_DICT


INPUT = open("advent2018_day19_input.txt", "r").read().split("\n")

ALTINPUT = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".split("\n")


# I used this when trying to deduce what the program did.  I printed my notes about each line when I executed it.
INPUT_EXPLAINED = """00: Jump to instruction 17
01: r[4] = 1
02: r[1] = 1
03: r[3] = r[4] * r[1]
04: r[3] = 1 if r[3] == r[5] else 0
05: Jump to instruction 7 if r[5] == r[4] * r[1]
06: Jump to instruction 8
07: r[0] += r[4]
08: r[1] += 1
09: r[3] = 1 if r[1] > r[5] else 0
10: Jump to instruction 12 if r[1] > r[5]
11: Jump to instruction 3
12: r[4] += 1
13: r[3] = 1 if r[4] > r[5] else 0
14: Jump to instruction 16 if r[4] > r[5]
15: Jump to instruction 2
16: Jump to instruction 256.  Exit condition?
17: r[5] += 2
18: r[5] = r[5]^2
19: r[5] *= 19
20: r[5] *= 11
21: r[3] += 8
22: r[3] *= 22
23: r[3] += 3
24: r[5] += r[3]
25: Add register 0 to the program counter
26: Jump to instruction 1
27: r[3] = 27
28: r[3] *= 28
29: r[3] += 29
30: r[3] *= 30
31: r[3] *= 14
32: r[3] *= 32
33: r[5] += r[3]
34: r[0] = 0
35: Jump to instruction 1""".split('\n')


def parse_input(lines):
    ip = int(lines[0].split(" ")[-1])
    instructions = []
    for line in lines[1:]:
        opcodes = [int(x) if x[0] not in string.ascii_letters else x for x in line.split(" ")]
        instructions.append(opcodes)
    return ip, instructions


def part_one(input_lines):
    ip_reg_num, instructions = parse_input(input_lines)

    registers = [0, 0, 0, 0, 0, 0]
    pc = registers[ip_reg_num]
    iteration = 0
    while 0 <= pc < len(instructions):
        iteration += 1
        registers[ip_reg_num] = pc
        opcode = instructions[pc]
        registers = OPCODE_DICT[opcode[0]](opcode, registers)
        pc = registers[ip_reg_num]
        pc += 1
    return registers


# Efficient factorization code shamelessly pulled from https://stackoverflow.com/a/6800214
def factors(n):
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


# The program explained
# number_to_factor = 1017
# if part_two_flag is set:
#     number_to_factor += 10550400 (for a total of 10551417)
# for i in xrange(1, number_to_factor):
#     for j in xrange(1, number_to_factor):
#         if i*j == number_to_factor:
#             result += j
# return result
#
# Thus, once we have the number to factor, we can calculate the result simply by sum(factor(number)).
def part_two(input_lines):
    ip_reg_num, instructions = parse_input(input_lines)
    registers = [1, 0, 0, 0, 0, 0]
    pc = registers[ip_reg_num]
    iteration = 0
    while 0 <= pc < len(instructions):
        iteration += 1
        registers[ip_reg_num] = pc
        if pc == 35:
            registers[0] = sum(factors(registers[5]))
            break
        opcode = instructions[pc]
        registers = OPCODE_DICT[opcode[0]](opcode, registers)
        pc = registers[ip_reg_num]
        pc += 1
    return registers


final_registers = part_one(INPUT)
print("Final part one register 0: %d" % final_registers[0])

final_registers = part_two(INPUT)
print("Final part two register 0: %d" % final_registers[0])
