from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def wrap_length(short1, short2):
    return short1 * 2 + short2 * 2
    
def bow_length(l,w,h):
    return l*w*h

def compute(s: str) -> int:

    boxes = s.splitlines()
    ribbon_list = []
    for box in boxes:
        coords = sorted([int(measure) for measure in box.split('x')])
        l,w,h = coords
        req = wrap_length(l,w) + bow_length(l,w,h)
        ribbon_list.append(req)
    return sum(ribbon_list)


INPUT_S = '''\
2x3x4
1x1x10
'''
EXPECTED = 48


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
