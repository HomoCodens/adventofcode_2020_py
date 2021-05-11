import numpy as np

def prepare(input):
    lines = input.splitlines()
    p1 = 1
    while lines[p1] != '':
        p1 += 1
    p1_cards = [int(x) for x in lines[1:p1]]
    p2_cards = [int(x) for x in lines[(p1+2):]]

    return (p1_cards, p2_cards)

def play(p1, p2):
    p1 = [x for x in p1]
    p2 = [x for x in p2]
    i = 0
    while len(p1) > 0 and len(p2) > 0:
        i += 1
        print(f'round {i}')
        print(f'me deck: {p1}')
        print(f'crab deck: {p2}')
        print(f'me cart: {p1[0]}')
        print(f'crabs cart: {p2[0]}')
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if c1 > c2:
            print('i win')
            p1 = p1 + [c1, c2]
        else:
            print('crab win')
            p2 = p2 + [c2, c1]

        print()

    winningdeck = p1 if len(p1) > 0 else p2
    print(winningdeck)
    print(np.flip(np.arange(len(winningdeck)) + 1))
    return np.sum(np.array(winningdeck) * np.flip(np.arange(len(winningdeck)) + 1))

def play_rec(p1, p2, level = 0):
    #p1 = [x for x in p1]
    #p2 = [x for x in p2]

    prev_states = {}
    while len(p1) > 0 and len(p2) > 0:
        # Anti infinity (gauntlet) rule
        quote_hash_quote = (str(p1), str(p2))
        if quote_hash_quote in prev_states:
            # TODO: Why is this an oops? (excercise for the reader)
            return True

        prev_states[quote_hash_quote] = 1

        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if len(p1) >= c1 and len(p2) >= c2:
            # STILL not a fan of that rangeing...
            p1_wins = play_rec(p1[:c1], p2[:c2], level + 1)
        else:
            p1_wins = c1 > c2
        
        if p1_wins:
            p1 = p1 + [c1, c2]
        else:
            p2 = p2 + [c2, c1]

    # TODO: SOC
    if level > 0:
        return len(p1) > 0
    else:
        print(f'btb: {"player1" if len(p1) > 0 else "player2"} winned')
        winningdeck = p1 if len(p1) > 0 else p2
        return np.sum(np.array(winningdeck) * np.flip(np.arange(len(winningdeck)) + 1))

def part_a(decks):
    p1, p2 = decks
    return play(p1[:], p2[:])

def part_b(decks):
    p1, p2 = decks
    return play_rec(p1, p2)

if __name__ == '__main__':
    example1 = prepare('''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
''')

    print(example1)
    #print(part_a(example1))
    print(part_b(example1))