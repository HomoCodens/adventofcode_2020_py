import re
import copy
import itertools

def line_to_ingredients(line):
    m = re.match(r'(?P<ingredients>.*?) \(contains (?P<allergens>.*?)\)', line)
    g = m.groupdict()
    return {
        'ingredients': g['ingredients'].split(),
        'allergens': g['allergens'].split(', ')
    }

def prepare(input):
    return [line_to_ingredients(l) for l in input.splitlines()]

def part_a(ingredients):
    working_set = copy.deepcopy(ingredients)
    all_the_allergens = set(itertools.chain.from_iterable([x['allergens'] for x in working_set]))
    print(all_the_allergens)


    known_allergens = {}
    unknown_allergens = [a for a in all_the_allergens]

    while len(known_allergens) < len(all_the_allergens):
        for a in unknown_allergens:
            s = None
            for product in working_set:
                if a in product['allergens']:
                    if s is None:
                        s = set(product['ingredients'])
                    else:
                        s = s.intersection(set(product['ingredients']))

                if s is not None and len(s) == 0:
                    break

            if len(s) == 1:
                # TODO
                ingredient = [x for x in s][0]
                print(f'finded out that {ingredient} means {a}')
                known_allergens[a] = ingredient
                for p in working_set:
                    # ye'd think I didn't care, wouldntye?
                    if ingredient in p['ingredients']:
                        p['ingredients'].remove(ingredient)
                unknown_allergens.remove(a)
                break

    print('cheap part 2:')
    allergens = [x for x in known_allergens.keys()]
    allergens.sort()
    print(allergens)
    print(known_allergens)
    print(','.join([known_allergens[a] for a in allergens]))
    return sum([len(x['ingredients']) for x in working_set])

if __name__ == '__main__':
    example1 = prepare('''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
''')
    print(part_a(example1))

