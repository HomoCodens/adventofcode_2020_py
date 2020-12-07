import networkx as nx
import re

def line_to_edgelist(line):
    # TODO: wrangle this into a single expression
    parent_id = re.match(r'^(.*) bags contain', line).groups()[0]
    childs = re.findall(r'(\d+) (.*?) bag[s]?', line)

    return [(parent_id, c[1], {'weight': int(c[0])}) for c in childs]

def prepare(rules):
    G = nx.DiGraph()
    for l in rules.splitlines():
        G.add_edges_from(line_to_edgelist(l))

    return G

def part_a(graph):
    encountered = []
    edge = list(graph.predecessors('shiny gold'))
    while True:
        n = edge.pop()
        encountered.append(n)
        for ng in graph.predecessors(n):
            edge.append(ng)
        if len(edge) == 0:
            break
    return len(set(encountered))

def dive(graph, node, cum_weight):
    s = 0
    for ng in graph.out_edges(node, True):
        s += cum_weight * ng[2]['weight']
        s += dive(graph, ng[1], cum_weight * ng[2]['weight'])
    return s

def part_b(graph):
    return dive(graph, 'shiny gold', 1)


if __name__ == '__main__':
    example1 = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''

    example2 = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
'''

    G = prepare(example1)
    assert part_a(G) == 4

    assert part_b(G) == 32

    assert part_b(prepare(example2)) == 126

    print('Day 7 all bagged up')