import re

def gen_document(data):
    doc = {}
    for pair in [x.split(':') for x in data.split()]:
        doc[pair[0]] = pair[1]
    return doc

def prepare(batch):
    start = 0
    end = 0
    docs = []
    lines = batch.splitlines()
    lines.append('')
    for l in lines:
        if l == '':
            docs.append(gen_document(' '.join(lines[start:end])))
            start = end
        end += 1
    return docs


def validate_fields(doc, verbose = False):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    passport_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    has_all_fields =  set(required_fields) == set(doc.keys()) or set(passport_fields) == set(doc.keys())
    
    if verbose:
        print(f'Has all required fields: {has_all_fields}')
    
    return has_all_fields

def validate_number(nmbr_in, min, max, verbose = False):
    nmbr = int(nmbr_in)

    if verbose:
        if nmbr is None:
            print(f'Not a valid number: {nmbr_in}')
        elif nmbr < min or nmbr > max:
            print(f'Number outside of range: {nmbr}, [{min}, {max}]')
        else:
            print(f'number is ok {min} <= {nmbr} <= {max}')

    return nmbr is not None and nmbr >= min and nmbr <= max

def validate_regex(field_in, pattern, verbose = False):
    match = re.match(pattern, field_in)
    if verbose:
        if match is None:
            print(f'{field_in} failed to match {pattern}')
        else:
            print('Regex match ok')

    return match

def validate_height(height, verbose = False):
    match = validate_regex(height, r'(?P<hgt>\d+)(?P<unit>(cm|in))')
    if match is None:
        return False

    groups = match.groupdict()
    if groups['unit'] == 'cm': # 'cause metric should always come first
        return validate_number(groups['hgt'], 150, 193, verbose)
    elif groups['unit'] == 'in':
        return validate_number(groups['hgt'], 59, 76, verbose)

    return False # Appease the unreachable code gods (and edge cases *shrug*)

validators = {
    'byr': lambda byr, verbose = False : validate_number(byr, 1920, 2002, verbose),
    'iyr': lambda iyr, verbose = False : validate_number(iyr, 2010, 2020, verbose),
    'eyr': lambda eyr, verbose = False : validate_number(eyr, 2020, 2030, verbose),
    'hgt': lambda hgt, verbose = False : validate_height(hgt, verbose),
    'hcl': lambda hcl, verbose = False : validate_regex(hcl, r'^#[0-9a-f]{6}$', verbose) is not None,
    'ecl': lambda ecl, verbose = False : validate_regex(ecl, r'^(amb|blu|brn|gry|grn|hzl|oth)$', verbose) is not None,
    'pid': lambda pid, verbose = False : validate_regex(pid, r'^\d{9}$', verbose) is not None
}

def validate_document(doc, part, verbose = False):
    if verbose:
        print(doc)

    fields = validate_fields(doc, verbose)
    if part == 1 or not fields:
        return fields
    
    for field in validators.keys():
        if verbose:
            print(f'checking field {field}')

        if not validators[field](doc[field], verbose):
            if verbose:
                print('Rejecting!')
            return False

    return True

def part_a(docs):
    # Summing booleans NEVER gets old ;P
    return sum([validate_document(x, 1) for x in docs])

def part_b(docs):
    return sum([validate_document(x, 2) for x in docs])

if __name__ == '__main__':
    example1 = prepare('''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
''')

    invalid_docs = prepare('''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
''')

    valid_docs = prepare('''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
''')

    assert part_a(example1) == 2

    assert validators['byr'](2002)
    assert not validators['byr'](2003)

    assert validators['hgt']('60in')
    assert validators['hgt']('190cm')
    assert not validators['hgt']('190in')
    assert not validators['hgt']('190')

    assert validators['hcl']('#123abc')
    assert not validators['hcl']('#123abz')
    assert not validators['hcl']('123abc')

    assert validators['ecl']('brn')
    assert not validators['ecl']('wat')

    assert validators['pid']('000000001')
    assert not validators['pid']('0123456789')

    assert part_b(invalid_docs) == 0
    assert part_b(valid_docs) == 4

    print('Day 4 pass')
