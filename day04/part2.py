from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def any_within(range1, range2):
    """Test to see if range1 falls at least partially within range2"""
    r1_initial, _ = range1.split("-")
    r2_initial, r2_final = range2.split("-")
    return int(r1_initial) >= int(r2_initial) and int(r1_initial) <= int(r2_final)


def any_overlaps(range1, range2):
    return any_within(range1,range2) or any_within(range2,range1)

def compute(s: str) -> int:

    lines = s.splitlines()
    overlapping_count = 0
    for line in lines:
        assign1, assign2 = line.split(",")
        if any_overlaps(assign1, assign2):
            overlapping_count += 1
    return overlapping_count


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 4


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
