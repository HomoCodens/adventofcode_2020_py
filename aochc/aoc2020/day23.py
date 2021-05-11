def prepare(input):
    return [int(x) for x in input.strip()]

def doit(sequence, n_values, times):
    if len(sequence) < n_values:
        sequence = sequence + list(range(max(sequence) + 1, n_values + 1))
    state = [{
        'number': x[1],
        'at': x[0],
        'next': x[0] + 1
    } for x in enumerate(sequence)]


    state[-1]['next'] = 0

    if n_values <= 20:
        crawly_print(state, state[0]['number'])
    
    lookup = len(state)*[None]
    for x in state:
        lookup[x['number'] - 1] = x

    current = state[0]
    for i in range(times):
        first_removed = state[current['next']]

        # shites and giggles
        nmbrs_removed = [
            first_removed['number'],
            state[first_removed['next']]['number'],        
            state[state[first_removed['next']]['next']]['number']
        ]
        
        last_removed = lookup[nmbrs_removed[-1] - 1]
        after_removed = state[last_removed['next']]

        target_n = current['number']
        while True:
            target_n -= 1
            if target_n == 0:
                target_n = n_values
            if not target_n in nmbrs_removed:
                break

        target = lookup[target_n - 1]

        after_target = state[target['next']]

        target['next'] = first_removed['at']
        last_removed['next'] = after_target['at']
        current['next'] = after_removed['at']
        current = state[current['next']]
        
        if n_values <= 20:
            print()
            print(f'-- move {i+2} --')
            crawly_print(state, current['number'])
        elif (i % 10000) == 0:
            print(i, flush = True)
    return (state, lookup)

def crawly_print(state, current_number):
    st = ''
    ii = 0
    for i in range(len(state)):
        x = state[ii]['number']
        st_x = '(' + str(x) + ')' if x == current_number else str(x)
        st += st_x + ' '
        ii = state[ii]['next']
    print(st)

def part_a(numbers):
    state, lookup = doit(numbers, len(numbers), 100)
    x = lookup[0]
    st = ''
    for i in range(len(numbers) - 1):
        x = state[x['next']]
        st += str(x['number'])
    return st

def part_b(numbers):
    state, lookup = doit(numbers, 1000000, 10000000)
    one = lookup[0]
    one_next = state[one['next']]
    one_next_next = state[one_next['next']]

    print(one)
    print(one_next)
    print(one_next_next)

    return one_next['number']*one_next_next['number']

if __name__ == '__main__':
    example1 = prepare('''389125467
''')

    print(part_b(example1))