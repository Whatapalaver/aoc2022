from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    chars = list(s)
    for i in range(len(chars) - 4):
        chunk = chars[i:i+4]
        # print(chunk, set(chunk), len(set(chunk)))
        if len(set(chunk)) == 4:
            return i + 4


INPUT_S = '''\
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
'''
EXPECTED = 11


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
