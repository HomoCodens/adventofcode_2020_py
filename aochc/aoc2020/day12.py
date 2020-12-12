import re
import numpy as np
import copy

def instruction_to_transform(instruction):
    m = re.match(r'([NESWRLF])(\d+)', instruction)
    g = m.groups()
    direction = g[0]
    distance = int(g[1])

    # Why? Why, why not?
    if direction in ['N', 'E', 'S', 'W']:
        heading = np.array([0, 1])
        if direction == 'S':
            heading = np.array([1, 0])
        elif direction == 'W':
            heading = np.array([0, -1])
        elif direction == 'N':
            heading = np.array([-1, 0])
        return {
            # Walk the Planck distance ye scurvy dog
            'execute': lambda s, part = 1: {
                'position': s['position'] + distance*heading,
                'heading': s['heading']
            } if part == 1 else {
                'position': s['position'],
                'heading': s['heading'] + distance*heading
            },
            'original': {
                'direction': direction,
                'distance': distance
            }
        }
    elif direction in ['R', 'L']:
        if direction == 'R':
            distance *= -1
        theta = np.radians(distance)
        c = np.cos(theta)
        s = np.sin(theta)
        R = np.round(np.array([[c, -s],[s, c]]))
        return {
            'execute': lambda s, part = 1: {
                'position': s['position'],
                'heading': R @ s['heading'] # @, sure...
            },
            'original': {
                'direction': direction,
                'distance': distance
            }
        }
    else:
        return {
            'execute': lambda s, part = 1: {
                'position': s['position'] + distance*s['heading'],
                'heading': s['heading']
            },
            'original': {
                'direction': direction,
                'distance': distance
            }
        }
    

def prepare(instructions):
    return [instruction_to_transform(i) for i in instructions.splitlines()]

def doit(instructions, part):
    ship = {
        'position': np.array([0, 0]),
        'heading': np.array([0, 1])
    }

    if part == 2:
        ship['heading'] = np.array([-1, 10])

    for i in instructions:
        ship = i['execute'](ship, part)
        # print(ship)
    return np.sum(np.abs(ship['position']), dtype = 'int32')

def part_a(instructions):
    return doit(instructions, 1)

def part_b(instructions):
    return doit(instructions, 2)

if __name__ == '__main__':
    example1 = '''F10
N3
F7
R90
F11
'''
    
    example1 = prepare(example1)
    assert part_a(example1) == 25
    assert part_b(example1) == 286

    print('TOOOOOOT')