import itertools
import numpy as np

def find_2020(data, n):
    combinations = itertools.combinations(data, n)
    for combi in combinations:
        if sum(list(combi)) == 2020:
            return np.prod(list(combi))

def prepare(raw):
    return [int(x) for x in raw]

def part_a(expenses):
    return find_2020(expenses, 2)

def part_b(expenses):
    return find_2020(expenses, 3)

if __name__ == '__main__':
    example1 = ['1721',
                '979',
                '366',
                '299',
                '675',
                '1456']

    example1_dat = prepare(example1)

    assert part_a(example1_dat) == 514579
    assert part_b(example1_dat) == 241861950

    print('Day 1 tests passed!')