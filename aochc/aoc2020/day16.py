import re
import numpy as np

def make_filter(line):
    m = re.match(
        r'^(?P<field>[a-z ]+): (?P<r1l>\d+)-(?P<r1u>\d+) or (?P<r2l>\d+)-(?P<r2u>\d+)',
        line
    )
    g = m.groupdict()
    r1l = int(g['r1l'])
    r1u = int(g['r1u'])
    r2l = int(g['r2l'])
    r2u = int(g['r2u'])
    return (g['field'], lambda x: (r1l <= x <= r1u) or (r2l <= x <= r2u))

def prepare(input):
    l = input.splitlines()
    li = 0

    filteurs = {}
    while l[li] != '':
        field, filter_function = make_filter(l[li])
        filteurs[field] = filter_function
        li += 1
    
    my_ticket = np.array([int(x) for x in l[li + 2].split(',')])

    nearby_tickets = np.array([[int(y) for y in x.split(',')] for x in l[(li+5):]])

    return {
        'filters': filteurs,
        'my_ticket': my_ticket,
        'nearby_tickets': nearby_tickets
    }

    

def part_a(data):
    tickets = data['nearby_tickets']
    filters = data['filters']

    invalid = []
    for ticket in tickets:
        for field in ticket:
            gud = False
            for fil in filters.values():
                gud = gud or fil(field)
            if not gud:
                invalid.append(field)
    return sum(invalid)

def is_ticket_valid(ticket, filters):
    for field in ticket:
        gud = False
        for fil in filters.values():
            gud = gud or fil(field)
        if not gud:
            return False
    return True

def part_b(data):
    filters = data['filters']
    print(len(data['nearby_tickets']))
    tickets = [t for t in data['nearby_tickets'] if is_ticket_valid(t, filters)]
    print(len(tickets))
    my_ticket = data['my_ticket']
    tickets.append(my_ticket) # can't hurtz, right?

    fields_to_find = [x for x in filters.keys()]
    known_fields = {}

    #stoeff = []
    #for ftf in fields_to_find:
    #    candidates = np.full(len(fields_to_find), True)
    #    for tick in tickets:
    #        ticket_map = np.array([filters[ftf](tf) for tf in tick])
    #        candidates = candidates & ticket_map
    #    stoeff.append(candidates)
    #stoeff.sort(key = lambda x: np.sum(x))
    #for st in stoeff:
    #    print(''.join(['1' if x else '0' for x in st]))

    while len(known_fields) < len(filters):
        gotone = False
        #print(fields_to_find)
        #print(known_fields)
        remaining_indices = np.setxor1d(np.arange(len(filters)), np.array([x for x in known_fields.values()], dtype = 'int32'))
        #print(remaining_indices)
        for ftf in fields_to_find:
            #print(ftf)
            candidates = np.full(len(fields_to_find), True)
            for tick in tickets:
                ticket_map = np.array([filters[ftf](tick[x]) for x in remaining_indices])
                candidates = candidates & ticket_map
            
            if np.sum(candidates) == 1:
                gotone = True
                at = remaining_indices[candidates][0]
                known_fields[ftf] = at
                fields_to_find.remove(ftf)
                print(f'finded out that field {ftf} lives at index {at}')
                break
        if not gotone:
            print('shite')
            break
    
    return np.prod([my_ticket[x[1]] for x in known_fields.items() if re.match(r'^departure', x[0])], dtype = 'int64')

    '''while len(known_fields) < len(filters):
        gotone = False
        print(known_fields)
        print(fields_to_find)
        mincand = 1000
        for ftf in fields_to_find:
            print(ftf)
            candidates = np.full(len(fields_to_find), True)
            #print([tf[0] for tf in enumerate(tickets[0]) if not tf[0] in known_fields.values()])
            for tick in tickets:
                ticket_map = np.array([filters[ftf](tf[1]) for tf in enumerate(tick) if not tf[0] in known_fields.values()])
                candidates = candidates & ticket_map
            if np.sum(candidates) == 2:
                print(candidates)
            if np.sum(candidates) < mincand:
                mincand = np.sum(candidates)
                mincandflags = candidates

            if np.sum(candidates) == 1:
                gotone = True
                at = np.where(candidates)[0][0]
                known_fields[ftf] = at
                fields_to_find.remove(ftf)
                break
        print(mincand)
        if not gotone:
            cands = np.array(fields_to_find)[mincandflags]
            wh = np.where(mincandflags)[0]
            print(wh)
            print(cands)
            print('agh, fail, throwing them out')
            for c in range(len(cands)):
                fields_to_find.remove(cands[c])
                known_fields[cands[c]] = wh[c]
            # break
    print(known_fields)'''



if __name__ == '__main__':
    example1 = prepare('''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
''')

    _, f = make_filter('field: 1-3 or 5-9')
    assert f(2)
    assert not f(10)

    assert part_a(example1) == 71

    example2 = prepare('''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
''')

    print([t for t in example1['nearby_tickets'] if is_ticket_valid(t, example1['filters'])])

    assert is_ticket_valid(example1['nearby_tickets'][0], example1['filters'])
    assert not is_ticket_valid(example1['nearby_tickets'][1], example1['filters'])

    #part_b(example2)