import re

def line_to_input(line):
    filetierer = re.compile(r'^(?P<from>\d+)-(?P<to>\d+) (?P<letter>.): (?P<password>.*)$')
    components = filetierer.match(line)
    return {
        'from': int(components.group('from')),
        'to': int(components.group('to')),
        'letter': components.group('letter'),
        'password': components.group('password')
    }

def prepare(input):
    return [line_to_input(l) for l in input.splitlines()]

def is_valid_sled(spec):
    letter_matches = sum([letter == spec['letter'] for letter in spec['password']])
    return letter_matches >= spec['from'] and letter_matches <= spec['to']

def is_valid_toboggan(spec):
    a = spec['password'][spec['from'] - 1]
    b = spec['password'][spec['to'] - 1]
    l = spec['letter']
    return (a == l or b == l) and not (a == l and b == l)

def part_a(specs):
    return sum([is_valid_sled(x) for x in specs])

def part_b(specs):
    return sum([is_valid_toboggan(x) for x in specs])

if __name__ == '__main__':
    example1 = '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''

    assert part_a(prepare(example1)) == 2
    assert part_b(prepare(example1)) == 1
    
    print('Day 2 Tests a-o-k-o')
