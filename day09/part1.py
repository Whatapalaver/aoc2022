from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

initial_tail = {(0, 0): 1}
tail_positions = defaultdict(lambda: 0, initial_tail)
PLANK_LENGTH = 1


def move_right(pos):
    return (pos[0] + 1, pos[1])

def move_left(pos):
    return (pos[0] - 1, pos[1])

def move_up(pos):
    return (pos[0], pos[1] + 1)

def move_down(pos):
    return (pos[0], pos[1] - 1)

def move_down_right(pos):
    new_pos = move_down(pos)
    return move_right(new_pos)

def move_down_left(pos):
    new_pos = move_down(pos)
    return move_left(new_pos)

def move_up_right(pos):
    new_pos = move_up(pos)
    return move_right(new_pos)

def move_up_left(pos):
    new_pos = move_up(pos)
    return move_left(new_pos)

def max_separation(tail_pos, head_pos):
    x_diff = head_pos[0] - tail_pos[0]
    y_diff = head_pos[1] - tail_pos[1]
    trajectory = "touching"
    max_separation = max(abs(x_diff), abs(y_diff))
    if max_separation > PLANK_LENGTH:
        if x_diff > 0 and y_diff > 0:
            trajectory = "UR"
        elif x_diff < 0 and y_diff > 0:
            trajectory = "UL"
        elif x_diff < 0 and y_diff < 0:
            trajectory = "DL"
        elif x_diff > 0 and y_diff < 0:
            trajectory = "DR"
        elif x_diff > 0:
            trajectory = "R"
        elif y_diff > 0:
            trajectory = "U"
        elif x_diff < 0:
            trajectory = "L"
        elif y_diff < 0:
            trajectory = "D"
    return max_separation, trajectory

def move_tail(tail_pos, trajectory):
    if trajectory == "touching":
        return tail_pos
    else:
        return movement_dict[trajectory](tail_pos)


movement_dict = {"R": move_right, "L": move_left, "U": move_up, "D": move_down, "UR": move_up_right, "UL": move_up_left, "DR": move_down_right, "DL": move_down_left}


def compute(s: str) -> int:
    lines = s.splitlines()
    current_head = (0, 0)
    current_tail = (0, 0)
    for line in lines:
        dir, steps_s = line.split(" ")
        steps = int(steps_s)
        for _ in range(steps):
            current_head = movement_dict[dir](current_head)
            sep, trajectory = max_separation(current_tail, current_head)
            current_tail = move_tail(current_tail, trajectory)
            tail_positions[current_tail] += 1

    return len(tail_positions)


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
