def parse_instruction(inst):
    s = inst.split()
    return (s[0], int(s[1]))

def prepare(instructions):
    return [parse_instruction(i) for i in instructions.splitlines()]

def step(state):
    p = state['pointer']
    i = state['instructions'][p]
    a = state['accumulator']
    
    if i[0] == 'nop':
        p += 1
    elif i[0] == 'jmp':
        p += i[1]
    elif i[0] == 'acc':
        a += i[1]
        p += 1

    return {
        'pointer': p,
        'instructions': state['instructions'], # Still a reference *shroog*
        'accumulator': a
    }

def run_to_halt(instructions):
    state = {
        'pointer': 0,
        'accumulator': 0,
        'instructions': instructions
    }

    pointerses = []
    while True:
        old_a = state['accumulator']
        state = step(state)
        p = state['pointer']

        if p == len(instructions):
            return (state['accumulator'], True)

        if p in pointerses:
            return (old_a, False)
        
        pointerses.append(state['pointer'])

def part_a(instructions):
    return run_to_halt(instructions)[0]

def part_b(instructions):
    for i in range(0, len(instructions)):
        if instructions[i][0] == 'jmp':
            instructions[i] = ('nop', instructions[i][1])
            result = run_to_halt(instructions)
            if result[1]:
                return result[0]
            instructions[i] = ('jmp', instructions[i][1])
        elif instructions[i][0] == 'nop':
            instructions[i]= ('jmp', instructions[i][1])
            result = run_to_halt(instructions)
            if result[1]:
                return result[0]
            instructions[i] = ('nop', instructions[i][1])

if __name__ == '__main__':
    example1 = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''

    assert part_a(prepare(example1)) == 5

    assert part_b(prepare(example1)) == 8

    print('Day nein, nein, nein, nein, nein...')