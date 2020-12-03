import numpy as np

def prepare(input):
    return np.array([list(x) for x in input])

def count_trees(map, right, down):
    n_rows, n_cols = map.shape
    r = np.array(range(down, n_rows, down))
    c = np.array(range(right, len(r)*right + right, right)) % n_cols
    return np.sum(map[r, c] == '#', dtype='int64')

def part_a(map):
    return count_trees(map, 3, 1)

def part_b(map):
    slopes = [[1, 1],
              [1, 3],
              [1, 5],
              [1, 7],
              [2, 1]]
    trees = 1
    for s in slopes:
        trees *= count_trees(map, s[1], s[0])
    return trees
    

if __name__ == '__main__':
    example1 = ['..##.......',
                '#...#...#..',
                '.#....#..#.',
                '..#.#...#.#',
                '.#...##..#.',
                '..#.##.....',
                '.#.#.#....#',
                '.#........#',
                '#.##...#...',
                '#...##....#',
                '.#..#...#.#']

    assert part_a(prepare(example1)) == 7
    assert part_b(prepare(example1)) == 336

    print('Day 3 working')
