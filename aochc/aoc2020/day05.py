import numpy as np

# NB: The whole row-seat thing is actually superfluous ^^
#     https://www.reddit.com/r/adventofcode/comments/k73xyd/day_5_part_1_in_7_bytes/
# Also:
#     In [17]: int('101', 2)
#     Out[17]: 5
def thing_to_number(x):
    bits = np.array([1 if l in ['B', 'R'] else 0 for l in x])
    pot = 2 ** np.array(range(len(x) - 1, -1, -1)) # *sigh*
    return sum(bits * pot)

def pass_to_seat(p):
    row_code = p[0:7]
    col_code = p[-3:]
    return (thing_to_number(row_code), thing_to_number(col_code))

def seat_id(seat):
    return 8*seat[0] + seat[1]

def prepare(passes):
    return [pass_to_seat(p) for p in passes.splitlines()]

def part_a(seats):
    return max([seat_id(s) for s in seats])

def part_b(seats):
    ids = [seat_id(s) for s in seats]
    first = min(ids)
    last = max(ids)
    return list(set(range(first, last)).difference(set(ids)))[0]


if __name__ == '__main__':
    assert part_a(prepare('FBFBBFFRLR\n')) == 357
    assert part_a(prepare('BFFFBBFRRR\n')) == 567
    assert part_a(prepare('FFFBBBFRRR\n')) == 119
    assert part_a(prepare('BBFFBBFRLL\n')) == 820

    print('Day 5 is GO')