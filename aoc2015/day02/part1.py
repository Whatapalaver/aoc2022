from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def surface_area(l,w,h):
    return 2*l*w + 2*w*h + 2*h*l

def slack(short1, short2):
    return short1 * short2

def compute(s: str) -> int:

    boxes = s.splitlines()
    area_list = []
    for box in boxes:
        coords = sorted([int(measure) for measure in box.split('x')])
        l,w,h = coords
        req = surface_area(l,w,h) + slack(l,w)
        area_list.append(req)
    return sum(area_list)


INPUT_S = '''\
2x3x4
1x1x10
'''
EXPECTED = 101


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
