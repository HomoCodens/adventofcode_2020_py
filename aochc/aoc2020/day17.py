# See also:
# http://drsfenner.org/blog/2015/07/game-of-life-in-numpy-preliminaries-2/
# http://drsfenner.org/blog/2015/08/game-of-life-in-numpy-2/
# However, building an (m, n, 3, 3) array every iteration may prove ungud

import numpy as np
from scipy import signal

def prepare(input):
    layer0 = np.array([[letter == '#' for letter in line] for line in input.splitlines()])
    return np.stack((np.full_like(layer0, False), layer0, np.full_like(layer0, False)))

def gro(generator):
    if np.any(generator[0, :, :]):
        print('growng up')
        generator = np.concatenate((np.full_like(generator, False), generator), 0)

    if np.any(generator[-1, :, :]):
        print('growng down')
        generator = np.concatenate((generator, np.full_like(generator, False)), 0)

    if np.any(generator[:, 0, :]):
        print('growng back')
        generator = np.concatenate((np.full_like(generator, False), generator), 1)

    if np.any(generator[:, -1, :]):
        print('growng forward')
        generator = np.concatenate((generator, np.full_like(generator, False)), 1)

    if np.any(generator[:, :, 0]):
        print('growng left')
        generator = np.concatenate((np.full_like(generator, False), generator), 2)

    if np.any(generator[:, :, -1]):
        print('growng right')
        generator = np.concatenate((generator, np.full_like(generator, False)), 2)

    return generator

def purdy_purnt(generator):
    for layer in generator:
        purdy_purnt_2d(layer)
    print('')

def purdy_purnt_2d(layer):
    for line in layer:
        print(''.join(['#' if x else '.' for x in line]))
    print('')

def part_a(generator):
    for i in range(6):
        generator = step(generator)

    return np.sum(generator)

def gro4(generator):
    if np.any(generator[0, :, :, :]):
        print('growng up')
        generator = np.concatenate((np.full_like(generator, False), generator), 0)

    if np.any(generator[-1, :, :, :]):
        print('growng down')
        generator = np.concatenate((generator, np.full_like(generator, False)), 0)

    if np.any(generator[:, 0, :, :]):
        print('growng back')
        generator = np.concatenate((np.full_like(generator, False), generator), 1)

    if np.any(generator[:, -1, :, :]):
        print('growng forward')
        generator = np.concatenate((generator, np.full_like(generator, False)), 1)

    if np.any(generator[:, :, 0, :]):
        print('growng left')
        generator = np.concatenate((np.full_like(generator, False), generator), 2)

    if np.any(generator[:, :, -1, :]):
        print('growng right')
        generator = np.concatenate((generator, np.full_like(generator, False)), 2)

    if np.any(generator[:, :, :, 0]):
        print('growng fleb')
        generator = np.concatenate((np.full_like(generator, False), generator), 3)

    if np.any(generator[:, :, :, -1]):
        print('growng glargh')
        generator = np.concatenate((generator, np.full_like(generator, False)), 3)

    return generator

def part_b(generator):
    generator = np.stack((np.full_like(generator, False), generator, np.full_like(generator, False)))

    for i in range(6):
        generator = step4(generator)
    return np.sum(generator)

def step4(generator):
    generator = gro4(generator)

    filt = np.full((3, 3, 3, 3), 1)
    filt[1, 1, 1, 1] = 0

    filtered = signal.convolve(generator, filt, 'same')

    return (filtered == 3) | (generator & (filtered == 2))

def step(generator):
    generator = gro(generator)

    filt = np.array([[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                     [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                     [[1, 1, 1], [1, 1, 1], [1, 1, 1]]])

    filtered = signal.convolve(generator, filt, 'same')

    # No growing up?ward. z axis is symmetrical anyway
    # filtered[0, :, :] = 0

    return (filtered == 3) | (generator & (filtered == 2))

if __name__ == '__main__':
    example1 = prepare('''.#.
..#
###
''')

    print(part_a(example1))
    print(part_b(example1))