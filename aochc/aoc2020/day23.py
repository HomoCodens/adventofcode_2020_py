# For those too lazy to mess with indices
from itertools import dropwhile, cycle, islice

def prepare(nmbrs):
    return [int(x) for x in nmbrs.strip()]

def step(numbers, current):
    #print(numbers)
    #print(current)

    n = len(numbers)
    rmvd = []
    rest = []
    i = 0
    for x in dropwhile(lambda x: x != current, cycle(numbers)):
        if x == current and len(rest) > 0:
            break
        
        if i in [1, 2, 3]:
            #print(f'putting {x} into removed')
            rmvd.append(x)
        else:
            #print(f'putting {x} into rest', flush=True)
            rest.append(x)

        i += 1

    #print(rmvd)
    #print(rest)

    nxt = current - 1
    #print(nxt)
    #print(nxt in rmvd)
    while nxt in rmvd or nxt == 0:
        #print(nxt, flush=True)
        nxt -= 1
        if nxt <= 0:
            nxt = n
    #print(f'next is {nxt}')

    nxt_state = []
    r = list(islice(dropwhile(lambda x: x != nxt, cycle(rest)), n - 3))
    #print(r)
    for x in r:
        #print(f'building with {x}')
        nxt_state.append(x)
        if x == nxt:
            #print(f'also, appending {rmvd}')
            nxt_state = nxt_state + rmvd
        
    #print(nxt_state)

    nxt_current = nxt
    picknext = False # Silly, i know
    for x in cycle(nxt_state):
        if x == current:
            picknext = True
        elif picknext:
            nxt_current = x
            break

    return (nxt_state, nxt_current)

def step_times(numbers, n):
    current = numbers[0]
    for i in range(n):
        numbers, current = step(numbers, current)
        print(i)
    return numbers

def part_a(numbers):
    numbers = step_times(numbers, 100)
    out = ''
    for x in list(islice(dropwhile(lambda x: x != 1, cycle(numbers)), 1, len(numbers))):
        out += str(x)
    return out

def part_b(numbers):
    m = max(numbers)
    numbers = numbers + list(range(m + 1, 1000001))
    step_times(numbers, 10)

if __name__ == '__main__':
    example1 = prepare('''389125467
''')

    print(part_a(example1))