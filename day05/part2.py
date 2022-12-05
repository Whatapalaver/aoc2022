from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Shameful handcranking of the stack map - life is too short!
TEST_STACK = [["Z","N"],["M","C","D"],["P"]]
INPUT_STACK = [["D","L","J","R","V","G","F"],["T","P","M","B","V","H","J","S"],["V","H","M","F","D","G","P","C"],["M","D","P","N","G","Q"],["J","L","H","N","F"],["N","F","V","Q","D","G","T","Z"],["F","D","B","L"],["M","J","B","S","V","D","N"],["G","L","D"]]

def compute(s: str, stack_map = INPUT_STACK) -> int:
    _, instructions = s.split("\n\n")

    lines = instructions.splitlines()
    for line in lines:
        _, ns, _, ss, _, ds = line.split()
        n = int(ns)
        source = int(ss)
        dest = int(ds)
        grab = stack_map[source-1][-n:]
        del stack_map[source-1][-n:]
        stack_map[dest-1].extend(grab)
    top = [stack[-1] if stack else '' for stack in stack_map]
    return ''.join(top)


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'MCD'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, TEST_STACK) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
