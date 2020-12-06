def prepare(answers):
    return ' '.join(answers.splitlines()).split('  ')

def get_n_yes_in_group(group_answers):
    return len(set([l for l in group_answers.replace(' ', '')]))

def get_n_everyone_yes(group_answers):
    individual_answers = [set([l for l in a]) for a in group_answers.split(' ')]
    all_yes = individual_answers[0]
    for i in range(1, len(individual_answers)):
        all_yes = all_yes & individual_answers[i]
    return len(all_yes)


def part_a(answers):
    return sum([get_n_yes_in_group(g) for g in answers])

def part_b(answers):
    return sum([get_n_everyone_yes(g) for g in answers])

if __name__ == '__main__':
    example1 = '''abc

a
b
c

ab
ac

a
a
a
a

b
'''
    assert part_a(prepare(example1)) == 11
    assert part_b(prepare(example1)) == 6
    print('Samichlaus says OK!')