def count_trees(map, right, down):
    n_rows = len(map)
    n_cols = len(map[0])
    row = 0
    col = 0
    trees = 0
    while row < n_rows - 1:
        row += down
        col = (col + right) % n_cols
        trees += map[row][col] == '#'
    return trees

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

    assert part_a(example1) == 7
    assert part_b(example1) == 336

    print('Day 3 working')