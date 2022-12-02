from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# AX = rock 1
# BY = paper 2
# CZ = scissors 3

results = {
    "A X": 4,
    "B Y": 5,
    "C Z": 6,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Z": 9,
    "C X": 7,
    "C Y": 2
}
        

def compute(s: str) -> int:
    lines = s.splitlines()
    scores = []
    for line in lines:
        scores.append(results[line])
    return sum(scores)


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
