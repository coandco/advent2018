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