def prepare(input):
    return [int(x) for x in input.splitlines()]

def validate_at(data, preamble_length, pos):
    # Preamble numbers are always valid
    if pos < preamble_length:
        return True

    if pos > len(data):
        raise 'No can do, boss'

    slc = data[(pos - preamble_length):pos]
    target = data[pos]

    for i in range(0, preamble_length - 1):
        for j in range(i + 1, preamble_length):
            if slc[i] + slc[j] == target:
                return True

    return False

def find_invalid(data, preamble_length):
    for i in range(preamble_length, len(data)):
        if not validate_at(data, preamble_length, i):
            return data[i]

def smash(data, weakness):
    n_data = len(data)
    for size in range(2, n_data):
        for start in range(0, n_data - size):
            slc = data[start:(start + size)]
            if sum(slc) == weakness:
                return min(slc) + max(slc)

    return -1

def part_a(data):
    return find_invalid(data, 25)

def part_b(data):
    return smash(data, find_invalid(data, 25))

if __name__ == '__main__':
    example1 = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
'''
    data = prepare(example1)

    assert find_invalid(data, 5)) == 127

    assert smash(data, find_invalid(data, 5)) == 62

    print('Git thee, I am day nine!')