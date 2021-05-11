def prepare(input):
    return input.splitlines()

def init_floor(paths):
    states = {}
    for p in paths:
        x, y, z = 0, 0, 0
        # No really, python has no proper looping...
        i = 0
        while i < len(p):
            instruction = p[i]
            if instruction in ['n', 's']:
                # Also, this:
                instruction = p[i:(i+2)]
                i += 1
            
            # AND THIS! Waaaaagh!
            if instruction == 'nw':
                z -= 1
                y += 1
            elif instruction == 'ne':
                z -= 1
                x += 1
            elif instruction == 'e':
                x += 1
                y -= 1
            elif instruction == 'se':
                z += 1
                y -= 1
            elif instruction == 'sw':
                z += 1
                x -= 1
            else:
                x -= 1
                y += 1

            i += 1
        
        pos = (x, y, z)
        if pos in states:
            states[pos] = not states[pos]
        else:
            states[pos] = True # ya know, False feels "blacker" though...
    
    return states

def part_a(paths):
    floor = init_floor(paths)
    return sum(floor.values())

def step_floor(floor): # get it? floors are for stepping on *laffs*
    # nw, ne, e, se, sw, w
    directions = [
        (0, 1, -1),
        (1, 0, -1),
        (1, -1, 0),
        (0, -1, 1),
        (-1, 0, 1),
        (-1, 1, 0)
    ]

    tiles_to_look_at = []
    for tile in floor.keys():
        x, y, z = tile
        tiles_to_look_at.append(tile)
        for d in directions:
            dx, dy, dz = d
            neighbour = (x + dx, y + dy, z + dz)
            tiles_to_look_at.append(neighbour)

    neighbours = {}
    for tile in set(tiles_to_look_at):
        x, y, z = tile
        n_black = 0
        for d in directions:
            dx, dy, dz = d
            neighbour = (x + dx, y + dy, z + dz)
            if neighbour in floor:
                n_black += floor[neighbour]
        neighbours[tile] = n_black
    
    new_floor = {}
    for tile in neighbours.keys():
        # tile is white
        if (not tile in floor) or (not floor[tile]):
            new_floor[tile] = (neighbours[tile] == 2)
        elif tile in floor and floor[tile]:
            new_floor[tile] = 0 < neighbours[tile] <= 2

    return new_floor

def part_b(paths):
    floor = init_floor(paths)
    for i in range(100):
        print(i, flush = True)
        floor = step_floor(floor)
    return sum(floor.values())

if __name__ == '__main__':
    example1 = prepare('''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
''')

    print(part_b(example1))