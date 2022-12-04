from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    overlaps = 0
    for line in lines:
        assign1, assign2 = line.split(",")
        a1_initial, a1_final = assign1.split("-")
        a2_initial, a2_final = assign2.split("-")
        if int(a1_initial) <= int(a2_initial) and int(a1_final) >= int(a2_final):
            overlaps += 1
        elif int(a2_initial) <= int(a1_initial) and int(a2_final) >= int(a1_final):
            overlaps += 1
    return overlaps


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
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
