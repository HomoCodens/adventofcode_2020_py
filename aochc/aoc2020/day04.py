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

required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
passport_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

def validate_document(doc, part):
    has_all_fields = set(required_fields) == set(doc.keys()) or set(passport_fields) == set(doc.keys())
    if part == 1 or not has_all_fields:
        #print('dont have the fields')
        return has_all_fields
    
    byr = int(doc['byr'])
    if byr < 1920 or byr > 2002:
        #print('fail at byr')
        return False

    iyr = int(doc['iyr'])
    if iyr < 2010 or iyr > 2020:
        #print('fail at iyr')
        #print(iyr)
        return False

    eyr = int(doc['eyr'])
    if eyr < 2020 or eyr > 2030:
        #print('fail at eyr')
        #print(eyr)
        return False

    hgt = doc['hgt']
    mtch = re.match(r'(?P<hgt>\d+)(?P<unit>(cm|in))', hgt)
    if mtch is None:
        #print('height wrong format')
        #print(hgt)
        return False
    else:
        print(hgt)
    grps = mtch.groupdict()
    unit = grps['unit']
    hgt = int(grps['hgt']) # And Rust goes WILD!

    if (unit == 'cm' and (hgt < 150 or hgt > 193)) or (unit == 'in' and (hgt < 59 or hgt > 76)):
        #print('fail at height')
        #print(doc['hgt']) # And Rust is (sort of) validated!!!
        return False
    else:
        print(doc['hgt'])
    hcl = doc['hcl']
    if re.match(r'^#[0-9a-f]{6}$', hcl) is None:
        #print('fail at hcl')
        #print(hcl)
        return False

    ecl = doc['ecl']
    if not ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        #print('fail at ecl')
        #print(ecl)
        return False

    pid = doc['pid']
    if not len(pid) == 9:
        #print('fail at pid')
        #print(pid)
        return False

    return True

def part_a(docs):
    return sum([validate_document(x, 1) for x in docs])

def part_b(docs):
    return sum([validate_document(x, 2) for x in docs])

if __name__ == '__main__':
    example1 = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
'''

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

    #print(invalid_docs)
    print([validate_document(x, 2) for x in invalid_docs])

    print([validate_document(x, 2) for x in valid_docs])

