from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    directions = list(s)
    print(directions)
    coord = (0,0)
    houses = set()
    houses.add(coord)
    print(houses)
    for dir in directions:
        x,y = coord
        if dir == '>':
            x += 1
        if dir == '<':
            x -= 1
        if dir == '^':
            y += 1
        if dir == 'v':
            y -= 1
        coord = (x,y)
        houses.add(coord)
    print(houses)
    return(len(houses))


INPUT_S = '''\
^v^v^v^v^v
'''
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
