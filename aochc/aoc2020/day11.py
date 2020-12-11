import numpy as np
from scipy import signal

import copy

def prepare(input):
    return np.array([[let for let in line] for line in input.splitlines()])

def purdy_purnt(waiting_area):
    for l in waiting_area:
        print(''.join(l))
    print('')

# Aw hell, I learned about them so why not?
def step_a(array):
    array = copy.deepcopy(array)
    filt = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    while True:
        occupied = array == '#'
        filtered = signal.convolve2d(occupied, filt, 'same')
        array[(array == 'L') & (filtered == 0)] = '#'
        array[(array == '#') & (filtered >= 4)] = 'L'
        yield copy.deepcopy(array)

def part_a(waiting_area, prnt = False):
    target = copy.deepcopy(waiting_area)
    for wa in step_a(waiting_area):
        if prnt:
            purdy_purnt(wa)
        if np.all(wa == target):
            return np.sum(wa == '#')
        target = wa

def get_n_free_neighbours_b(array, row, col):
    n = 8
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if not (dr == 0 and dc == 0):
                r = row + dr
                c = col + dc
                while r >= 0 and r < len(array) and c >= 0 and c < len(array[0]):
                    if array[r][c] == '#':
                        n -= 1
                        break
                    elif array[r][c] == 'L':
                        break
                    r += dr
                    c += dc
    return n

def step_b(array):
    next_step = copy.deepcopy(array)
    for r in range(0, len(next_step)):
        for c in range(0, len(next_step[0])):
            if not next_step[r][c] == '.':
                n_free = get_n_free_neighbours_b(array, r, c)
                if n_free == 8:
                    next_step[r][c] = '#'
                elif n_free <= 3:
                    next_step[r][c] = 'L'
    return next_step

def part_bb(waiting_area):
    prev = copy.deepcopy(waiting_area)
    waiting_area = step_b(waiting_area)
    while not np.all(prev == waiting_area):
        prev = copy.deepcopy(waiting_area)
        waiting_area = step_b(waiting_area)

    return np.sum(waiting_area == '#')

if __name__ == '__main__':
    example1 = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''
    #print(prepare(example1))
    #print(get_n_free_neighbours(prepare(example1), 1, 1))
    #print(step(prepare(example1)))
    #print(step(step(prepare(example1))))
    print(part_a(prepare(example1), prnt = True))


    example2 = prepare('''.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
''')

    example3 = prepare('''.............
.L.L.#.#.#.#.
.............
''')

    example4 = prepare('''.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
''')

    #print(get_n_free_neighbours_b(example2, 4, 3))
    #print(get_n_free_neighbours_b(example3, 1, 1))
    #print(get_n_free_neighbours_b(example4, 3, 3))
    #print(part_b(prepare(example1)))