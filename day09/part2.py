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

def move_body_knot(knot_pos, trajectory):
    if trajectory == "touching":
        return knot_pos
    else:
        return movement_dict[trajectory](knot_pos)
    
def move_rope_body(rope):
    rope = rope
    ch = rope[0]
    for i in range(1,10):
        # print(rope)
        # print(current_knot)
        current_knot = rope[i]
        prior_knot = rope[i-1]
        sep, trajectory = max_separation(current_knot, prior_knot)
        # print("next knot: ", move_body_knot(current_knot, trajectory))
        rope[i] = move_body_knot(current_knot, trajectory)
        
    return rope

movement_dict = {"R": move_right, "L": move_left, "U": move_up, "D": move_down, "UR": move_up_right, "UL": move_up_left, "DR": move_down_right, "DL": move_down_left}


def compute(s: str) -> int:
    lines = s.splitlines()
    current_head = (0, 0)
    rope = [(0,0) for _ in range(10)]
    for line in lines:
        dir, steps_s = line.split(" ")
        steps = int(steps_s)
        print("#######", dir, steps, "#######")
        print("Start: ", rope)
        for _ in range(steps):
            current_head = movement_dict[dir](current_head)
            rope[0] = current_head
            # move_rope_body and update rope_body
            rope = move_rope_body(rope)
            current_tail = rope[-1]
            tail_positions[current_tail] += 1
        print("End: ", rope)

    return len(tail_positions)


INPUT_S = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED = 36


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
