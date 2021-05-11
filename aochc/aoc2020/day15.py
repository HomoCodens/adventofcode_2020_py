def prepare(input):
    return [int(x) for x in input.split(',')]

def run_til(numbers, step):
    spoken = {}
    mrs = numbers[-1]

    for i in range(len(numbers)):
        #print(f'Elf says {numbers[i]}')
        spoken[numbers[i]] = i + 1

    for i in range(len(numbers), step):
        if mrs in spoken.keys():
            current = i - spoken[mrs]
        else:
            #print('new!')
            current = 0
        #print(f'Elf says {current} at {i}')
        spoken[mrs] = i
        mrs = current
    return mrs

def part_a(numbers):
    return run_til(numbers, 2020)

def part_b(numbers):
    return run_til(numbers, 30000000)

if __name__ == '__main__':
    example1 = prepare('0,3,6')
    example2 = prepare('1,3,2')
    example3 = prepare('2,1,3')
    example4 = prepare('1,2,3')
    example5 = prepare('2,3,1')
    example6 = prepare('3,2,1')
    example7 = prepare('3,1,2')

    #assert part_a(example1) == 436
    #assert part_a(example2) == 1
    #assert part_a(example3) == 10
    #assert part_a(example4) == 27
    #assert part_a(example5) == 78
    #assert part_a(example6) == 438
    assert part_a(example7) == 1836

    print('gut')