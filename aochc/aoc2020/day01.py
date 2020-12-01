def prepare(raw):
    return [int(x) for x in raw]

def part_a(expenses):
    n_exp = len(expenses)
    for i in range(0, n_exp-1):
        for j in range(i, n_exp):
            if expenses[i] + expenses[j] == 2020:
                return expenses[i]*expenses[j]
    
def part_b(expenses):
    n_exp = len(expenses)
    for i in range(0, n_exp-2):
        for j in range(i, n_exp-1):
            for k in range(j, n_exp):
                if expenses[i] + expenses[j] + expenses[k] == 2020:
                    return expenses[i]*expenses[j]*expenses[k]

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