def prepare(input):
    keys = [int(k) for k in input.splitlines()]
    return (keys[0], keys[1])

def find_loop_size(pk, mul):
    v = 1
    ls = 0
    while True:
        v = (v*mul) % 20201227
        ls += 1
        if (ls % 10000) == 0:
            print(ls, flush=True)
        if v == pk:
            return ls

def part_a(keys):
    card_key, door_key = keys

    ls_card = find_loop_size(card_key, 7)

    v = 1
    for i in range(ls_card):
        v = (v*door_key) % 20201227
    return v

if __name__ == '__main__':
    example1 = prepare('''5764801
17807724''')

    print(part_a(example1))