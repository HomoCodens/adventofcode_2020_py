from argparse import ArgumentParser
from datetime import datetime
import sys
import runpy
import os
import importlib

def run_one():
    parser = ArgumentParser(description='Advent of Code 2020')
    now = datetime.now()

    parser.add_argument(
        '-m', '--mod',
        action='store_true'
    )
    parser.add_argument(
        'day',
        nargs='?',
        type=int,
        choices=range(1, 26),
        default=min(now.day, 25) if now.month == 12 else 1,
        help='1-25 (default: %(default)s)',
    )
    parser.add_argument(
        'to',
        nargs='?',
        type=int,
        choices=range(1, 26),
        help='1-25 (default: %(default)s)',
    )
    args = parser.parse_args()

    if args.to is None:
        args.to = args.day

    if args.to < args.day:
        print('Second day must be larger an first!')
        sys.exit()

    for i in range(args.day, args.to + 1):
        module_name = f'aochc.aoc2020.day{i:02}'

        if args.mod:
            runpy.run_module(module_name, run_name='__main__')
        else:
            mod = importlib.import_module(module_name)
            mod_contents = dir(mod)

            prepare_data = False

            print(i)
            infile = os.path.join(os.path.dirname(__file__), 'aoc2020', 'input', f'day{i:02}.txt')
            with open(infile, 'r') as inf:
                data = inf.read()
                
            if 'prepare' in mod_contents:
                prepare_data = True

            if 'part_a' in mod_contents:
                p1 = mod.part_a(data if not prepare_data else mod.prepare(data))
            
                print('Part 1:', p1)

            if 'part_b' in mod_contents:
                p2 = mod.part_b(data if not prepare_data else mod.prepare(data))

                print('Part 2:', p2)

if __name__ == '__main__':
    run_one()