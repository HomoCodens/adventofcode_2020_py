# NB: The author is well aware of how to spell "tile" but just carried the typo forward
#     for the (personal) lulz

import re
import numpy as np
import copy
from scipy import signal

def prepare(input):
    tiels = []
    new_tile = True
    id = 0
    tile_liens = []
    for l in input.splitlines():
        if new_tile:
            m = re.match(r'Tile (\d+):', l)
            g = m.groups()
            id = int(g[0])
            new_tile = False
        elif l == '':
            tiels.append({
                'id': id,
                'data': np.array(tile_liens)
            })
            tile_liens = []
            new_tile = True
        else:
            tile_liens.append([x for x in l])
    
    tiels.append({
                'id': id,
                'data': np.array(tile_liens)
            })

    return tiels

def gen_edge_ids(tiel):
    d = tiel['data']
    ed = np.array([
        d[0, :],
        d[:, -1],
        d[-1, :],
        d[:, 0],
        np.flip(d[0, :]),
        np.flip(d[:, -1]),
        np.flip(d[-1, :]),
        np.flip(d[:, 0])
    ])
    ed_bin = [int(''.join(['1' if letter == '#' else '0' for letter in edge]), 2) for edge in ed]
    return ed_bin

def match_tiels(tiels):
    tiels = copy.deepcopy(tiels)
    for t in tiels:
        t['edge_ids'] = gen_edge_ids(t)
        t['neighbours'] = []

    for i in range(len(tiels) - 1):
        for j in range(i + 1, len(tiels)):
            a = tiels[i]
            b = tiels[j]
            if len(set(a['edge_ids']).intersection(set(b['edge_ids']))):
                a['neighbours'].append(b['id'])
                b['neighbours'].append(a['id'])

    return tiels

def part_a(tiels):
    tiels = match_tiels(tiels)
    corner_ids = [t['id'] for t in tiels if len(t['neighbours']) == 2]
    
    return np.prod(corner_ids, dtype='int64')

def strip_edge_tiel(tiel):
    return strip_edge_data(tiel['data'])

def strip_edge_data(data):
    return data[1:-1, 1:-1]

def prnt(tiel):
    print('\n'.join([''.join(l) for l in tiel]))
    print()

# Transformations for tile data
eye = lambda t: t
fH = lambda t: np.flipud(t)
fV = lambda t: np.fliplr(t)
fD = lambda t: fH(fV(t))
rCW = lambda t: np.rot90(t, 3)
rCCW = lambda t: np.rot90(t)
fVrCCW = lambda t: rCCW(fV(t))
fHrCCW = lambda t: rCCW(fH(t))

# Transform tile a so that is fits tile b
def adjust_a(a, b):
    transforms = [
        [fH, fVrCCW, eye, rCCW, fD, rCW, fV, fHrCCW],
        [fVrCCW, fV, rCW, eye, rCCW, fD, fHrCCW, fH],
        [eye, rCCW, fH, fVrCCW, fV, fHrCCW, fD, rCW],
        [rCW, eye, fVrCCW, fV, fHrCCW, fH, rCCW, fD],
        [fD, rCW, fV, fHrCCW, fH, fVrCCW, eye, rCCW],
        [rCCW, fD, fHrCCW, fH, fVrCCW, fV, rCW, eye],
        [fV, fHrCCW, fD, rCW, eye, rCCW, fH, fVrCCW],
        [fHrCCW, fH, rCCW, fD, rCW, eye, fVrCCW, fV]
    ]

    for eai in range(len(a['edge_ids'])):
        ea = a['edge_ids'][eai] # ...sports: it's in the game
        ebi = np.argwhere(ea == np.array(b['edge_ids']))
        if len(ebi) > 0:
            ebi = ebi[0][0]
            return (ebi % 4, transforms[ebi][eai](a['data']))
    return (-1, None)

def get_tiel_with_id(tiels, id):
    return [t for t in tiels if t['id'] == id][0]

def assemble_image(tiels):
    n_tiels = len(tiels)
    n_tiels_on_edge = int(np.round(np.sqrt(n_tiels)))
    tiel_shape = tiels[0]['data'].shape
    tiel_pixel_edge = tiel_shape[0] - 2

    # sounds yiddish, stands for image element ;P
    imels = np.full((n_tiels_on_edge, n_tiels_on_edge, tiel_pixel_edge, tiel_pixel_edge), '')

    corner_ids = [t['id'] for t in tiels if len(t['neighbours']) == 2]

    # Figure out which corner to start from
    tl = get_tiel_with_id(tiels, corner_ids[0])
    tld = tl['data']

    pos_0 = [0, 0]

    e1, _ = adjust_a(get_tiel_with_id(tiels, tl['neighbours'][0]), tl)
    e2, _ = adjust_a(get_tiel_with_id(tiels, tl['neighbours'][1]), tl)

    if e1 == 0 or e2 == 0:
        pos_0[0] = n_tiels_on_edge - 1
    if e1 == 3 or e2 == 3:
        pos_0[1] = n_tiels_on_edge - 1

    imels[pos_0[0], pos_0[1], :, :] = strip_edge_data(tld)
    edge = [tl['id']]
    done = []
    positions = {}
    positions[edge[0]] = pos_0

    while len(edge) > 0:
        current_id = edge.pop()
        current_tiel = get_tiel_with_id(tiels, current_id)
        pos_current = positions[current_id]

        for n in current_tiel['neighbours']:
            if not n in done and not n in edge:
                edge.append(n)
                neighbour_tiel = get_tiel_with_id(tiels, n)
                common_border, transformed = adjust_a(neighbour_tiel, current_tiel)
                if common_border == 0:
                    pos_neighbour = [pos_current[0] - 1, pos_current[1]]
                elif common_border == 1:
                    pos_neighbour = [pos_current[0], pos_current[1] + 1] 
                elif common_border == 2:
                    pos_neighbour = [pos_current[0] + 1, pos_current[1]]
                elif common_border == 3:
                    pos_neighbour = [pos_current[0], pos_current[1] - 1]
                else:
                    raise 'that ain\'t happening!'

                neighbour_tiel['data'] = transformed
                tiels = match_tiels(tiels)

                imels[pos_neighbour[0], pos_neighbour[1], :, :] = strip_edge_data(transformed)
                positions[n] = pos_neighbour
        done.append(current_id)
    image = np.concatenate(np.concatenate(imels, axis = 1), axis = 1)

    return image

def part_b(tiels):
    tiels = match_tiels(tiels)
    image = assemble_image(tiels)

    binimg = np.where(
        image == '#',
        np.full_like(image, 1, dtype = 'int8'),
        np.full_like(image, 0, dtype = 'int8'))
    maunster = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''

# easter bunny
#    maunster = ''' # # 
#  #  
# ### 
# ### 
#'''

# Sasqueti
#    maunster = '''  #  
######
# ### 
# # # 
#'''

    maunster_filter = [[1 if x == '#' else 0 for x in line] for line in maunster.splitlines()]
    n_cells_in_maunster = np.sum(maunster_filter)

    for tr in [eye, fH, fV, fD, rCW, rCCW, fVrCCW, fHrCCW]:
        filtered = np.array(signal.convolve2d(tr(binimg).tolist(), maunster_filter, 'same'))
        if np.any(filtered == n_cells_in_maunster):
            n_monsters = np.sum(filtered == n_cells_in_maunster)
            print(f'found {n_monsters} entities')
            # Wait, which one has precedence again? ^^
            return np.sum(binimg) - (n_monsters * n_cells_in_maunster)
    return -6

if __name__ == '__main__':
    example1 = prepare('''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
''')

    print(part_b(example1))