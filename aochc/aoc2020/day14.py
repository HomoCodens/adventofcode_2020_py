import re

def line_to_instruction(l):
    m = re.match(r'mem\[(?P<address>\d+)\] = (?P<value>\d+)', l)

    if m is not None:
        g = m.groupdict()
        return {
            'action': 'set',
            'address': int(g['address']),
            'value': int(g['value'])
        }
    else:
        mask = re.sub('mask = ', '', l)
        print(f'mask is {mask}')
        p1 = ''.join([x if x == '1' else '0' for x in mask])
        pass1 = int(p1, 2)
        print(f'pass1 is {p1}')
        p0 = ''.join(['0' if x == '0' else '1' for x in mask])
        pass0 = int(p0, 2)
        print(f'pass0 is {p0}')
        pf = ''.join(['0' if x in ['0', 'X'] else '1' for x in mask])
        passf = int(pf, 2)
        floaters = [x[0] for x in enumerate(mask) if x[1] == 'X']
        return {
            'action': 'mask',
            'pass1': pass1,
            'pass0': pass0,
            'passf': passf,
            'floating': floaters
        }

def prepare(input):
    return [line_to_instruction(l) for l in input.splitlines()]

def write(mem, at, value, mask):
    if mask is not None:
        value = (value & mask['pass0']) | mask['pass1']
    mem[at] = value
    return mem

def part_a(instructions):
    memory = {}
    mask = None
    for i in instructions:
        if i['action'] == 'mask':
            mask = i
        else:
            memory = write(memory, i['address'], i['value'], mask)
    return sum(memory.values())

def write2_(mem, at, value, floating, i):
    #print(f'write2_: at {at} write {value} ({floating} - {i})')

    if i == len(floating):
        print(f'writing {value} to address {at}')
        mem[at] = value
        return mem

    mask = 1 << (35 - floating[i])
    #print(mask)

    # write with floating bit high
    mem = write2_(mem, at, value, floating, i+1)

    # write with floating bit low
    mem = write2_(mem, at & ~mask, value, floating, i+1)


    return mem

def write2(mem, at, value, mask):
    if mask is None:
        mem[at] = value
        return mem

    print(f'start: {at:010b}')
    pf = mask['pass0']
    print(f"passf: {pf:010b}")
    at = at | pf
    print(f'after: {at:010b}')
    print(f'should {26:010b}')

    return write2_(mem, at, value, mask['floating'], 0)

def part_b(instructions):
    memory = {}
    mask = None
    for i in instructions:
        if i['action'] == 'mask':
            mask = i
        else:
            memory = write2(memory, i['address'], i['value'], mask)
    print(memory)
    return sum(memory.values())

if __name__ == '__main__':
    example1 = prepare('''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
''')

    print(part_a(example1))

    example2 = prepare('''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
''')

    print(example2)
    print(part_b(example2))