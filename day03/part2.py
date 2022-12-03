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
    unique_items = [set(line) for line in lines]
    priority_scores = []
    # process in groups of 3
    for i in range(0, len(unique_items), 3):
        group = unique_items[i:i+3]
        group_overlap = group[0].intersection(group[1],group[2])
        score = sum([gift_types.index(gift) + 1 for gift in group_overlap])
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
EXPECTED = 70


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
