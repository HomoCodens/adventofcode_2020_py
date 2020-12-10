import numpy as np

def prepare(input):
    joltages = [int(x) for x in input.splitlines()]
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    return np.sort(np.array(joltages))

def recurshian(joltages, start):
    if start == len(joltages) - 1:
        return True

    s = 0
    for i in range(start + 1, min(len(joltages), start + 4)): # I find this non-inclusive ranging silly
        if joltages[i] - joltages[start] <= 3:
            s += recurshian(joltages, i)

    return s

def part_a(joltages):
    _, counts = np.unique(np.diff(joltages), return_counts = True)
    return counts[0]*counts[-1] # Blatantly assuming there are at least 1 1 and 1 3 jolt diff

def part_b(joltages):
    # TODO: Do this diff like
    skippables = np.zeros_like(joltages)
    for i in range(0, len(joltages)):
        for j in range(i + 2, min(len(joltages), i + 4)):
            if joltages[j] - joltages[i] <= 3:
                skippables[i] += 1

    thingenses = []

    i = 0
    while i < len(skippables):
        if skippables[i] > 0:
            start = i
            end = i+1
            for j in range(i, len(skippables)):
                if skippables[j] == 0:
                    end = j + 2
                    i = end - 1
                    break
            thingenses.append(recurshian(joltages[start:end], 0))
        i += 1

    # Curse you and your big numbers, Eric!
    return np.prod(thingenses, dtype = 'int64')

if __name__ == '__main__':
    example1 = '''16
10
15
5
1
11
7
19
6
12
4
'''

    example2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''
    
    assert part_a(prepare(example1)) == 35
    assert part_a(prepare(example2)) == 220

    assert part_b(prepare(example1)) == 8
    assert part_b(prepare(example2)) == 19208

    print('Double digits!')