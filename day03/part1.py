from __future__ import annotations

import argparse
import os.path

import pytest

import support
import string
import math

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

gift_types = string.printable[10:62]

def compute(s: str) -> int:

    lines = s.splitlines()
    priority_scores = []
    for line in lines:
        length = len(line)
        mid = math.floor(length/2)
        comp1 = line[:mid]
        comp2 = line[mid:]
        uniq1 = set(comp1)
        uniq2 = set(comp2)
        overlap = uniq1.intersection(uniq2)
        score = sum([gift_types.index(gift) + 1 for gift in overlap])
        priority_scores.append(score)
    return sum(priority_scores)


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 157


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
