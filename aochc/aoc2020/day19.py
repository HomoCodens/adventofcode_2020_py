from lark import Lark
import re

def prepare(input):
    lines = input.splitlines()

    r1 = 0
    while lines[r1] != '':
        r1 += 1

    rules = [re.sub(r'(\d+)', r'id\1', l) for l in lines[:r1]]

    return {
        'rules': rules,
        'words': lines[(r1+1):]
    }

def part_a(problem):
    xx = Lark('\n'.join(problem['rules']), start = 'id0')
    s = 0
    for w in problem['words']:
        try:
            xx.parse(w)
            s += 1
        except:
            next
    return s

def part_b(problem):
    new_rules = []
    for r in problem['rules']:
        if r == 'id8: id42':
            print('blerb')
            new_rules.append('id8: id42 | id42 id8')
        elif r == 'id11: id42 id31':
            print('blorb')
            new_rules.append('id11: id42 id31 | id42 id11 id31')
        else:
            new_rules.append(r)

    xx = Lark('\n'.join(new_rules), start = 'id0')
    s = 0
    for w in problem['words']:
        try:
            xx.parse(w)
            s += 1
        except:
            next
    return s

if __name__ == '__main__':
    json_parser = Lark(r"""
    value: dict
         | list
         | ESCAPED_STRING
         | SIGNED_NUMBER
         | "true" | "false" | "null"

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : ESCAPED_STRING ":" value

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='value')

    text = '{"key": ["item0", "item1", 3.14]}'
    print(json_parser.parse(text).pretty())

    e1 = prepare('''0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aaaa''')

    print(part_a(e1))