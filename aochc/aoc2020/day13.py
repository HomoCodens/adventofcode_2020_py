# In which we repeadedly run into walls, prove we can (almost)
# implement an algorithm from wikipedia, fear losing our mind,
# contemplate cheating with a c&p solution and finally find some kind of peace

import numpy as np
from functools import reduce
#import pulp as fiction # come on!
#from scipy import optimize
#import os

def prepare(input):
    notes = input.splitlines()
    return {
        'at_bus_stop': int(notes[0]),
        # Not filtering times because _of course_ they are meaningless ;P
        'bus_times': np.array([None if x == 'x' else int(x) for x in notes[1].split(',')])
    }

def part_a(notes):
    arrival_me = notes['at_bus_stop']
    bus_times = notes['bus_times']
    in_service = bus_times[bus_times != None]
    next_catchable_trip = (np.floor(arrival_me / in_service) + 1) * in_service
    waits = next_catchable_trip - arrival_me
    the_one = np.argmin(waits)
    return waits[the_one] * in_service[the_one]

def extended_euclidian(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r > 0:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    return (old_s, old_t)

def zipperer(a, b):
    na, aa = a
    nb, ab = b
    print(f'zipperering n = {[na, nb]}, a = {[aa, ab]}')
    x = chinese_remainder_two([na, nb], [aa, ab])
    nanb = na*nb
    print(f'returning {(nanb, x % nanb)}')
    return (nanb, x % nanb)

# You must say this in a you-know-who voice
def chinese_remainder(n, a):
    ub = reduce(zipperer, zip(n, a))
    return ub[1]

def chinese_remainder_two(n, a):
    m1, m2 = extended_euclidian(n[0], n[1])
    x = a[0]*m2*n[1] + a[1]*m1*n[0]
    return x

def part_b(notes, init = None):
    bus_times = notes['bus_times']
    times = bus_times[bus_times != None]
    offsets = times - np.arange(len(bus_times))[bus_times != None]

    #pos, increment = 0, times[0]
    #for offset, time in zip(offsets[1:], times[1:]):
    #    while (pos + offset) % time != 0:
    #        pos += increment
#
    #    increment *= time
#
    #return pos

#
    #print([x for x in zip(times, offsets)])
#
    return chinese_remainder(times, offsets)

    #p = fiction.LpProblem('aoc', sense = fiction.LpMinimize)
#
    #x = fiction.LpVariable.dicts('x', times, lowBound = 0, cat = 'Integer')
#
    #p += times[0]*x[times[0]]
#
    #for i in range(1, len(times)):
    #    p += times[i]*x[times[i]] - times[0]*x[times[0]] == offsets[i]
#
    #if init is not None:
    #    x[times[0]].setInitialValue(np.floor(init / times[0]))
#
    #p.writeLP(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bla.lp'))
    #p.solve()
#
    #print(p)
    #for v in p.variables():
    #    if v.varValue>0:
    #        print(v.name, "=", v.varValue)
#
    #return fiction.value(p.objective)

    #c = times
    #b_eq = offsets
    #A_eq = np.diag(times)
    #A_eq[:, 0] -= times[0]
    #print(A_eq)

    #x = optimize.linprog(c, A_eq = A_eq, b_eq = b_eq)
    #print(x)

    #ORDEEER = np.flip(np.argsort(times))
    #times = times[ORDEEER]
    #offsets = offsets[ORDEEER]
    #print(times)
    #print(offsets)
    #
    #tt = 0
    #while True:
    #    tt += times[0]
    #    t = tt - offsets[0]
    #    if tt % (1000000 * times[0]) == 0:
    #        print(tt, flush = True)
    #    gud = True
    #    for i in np.arange(1, len(offsets)):
    #        # print(f'testing for {times[i]} - tt = {t + offsets[i]} - remainder = {(t + offsets[i]) % times[i]}')
    #        if (t + offsets[i]) % times[i] != 0:
    #            gud = False
    #            break
    #    if gud:
    #        print(f'found a gud: {t}')
    #        return t

if __name__ == '__main__':
    example1 = prepare('''939
7,13,x,x,59,x,31,19
''')

    assert part_a(example1) == 295

    assert part_b(example1) == 1068781

    example2 = prepare('''0
17,x,13,19''')

    example3 = prepare('''0
67,7,59,61''')

    example4 = prepare('''0
67,x,7,59,61''')

    example5 = prepare('''0
67,7,x,59,61''')

    example6 = prepare('''0
1789,37,47,1889''')

    assert part_b(example2) == 3417
    assert part_b(example3) == 754018
    assert part_b(example4) == 779210
    assert part_b(example5) == 1261476
    assert part_b(example6) == 1202161486
