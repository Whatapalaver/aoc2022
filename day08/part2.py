from __future__ import annotations
from collections import defaultdict

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
wood = []
tree_map = {}
scenic_scores = defaultdict(lambda: 0)

def is_edge(point):
    no_of_cols = len(wood[0])
    no_of_rows = len(wood)
    row_idx = point[1]
    col_idx = point[0]
    if row_idx == 0 or row_idx == no_of_rows-1:
        return True 
    elif col_idx == 0 or col_idx == no_of_cols-1:
        return True
    else:
        return False

    
def get_look_left(point):
    col_idx, row_idx = point
    row = wood[row_idx]
    visible_row = row[:col_idx]
    visible_row.reverse()
    # print("left: ", visible_row)
    return visible_row

def get_look_right(point):
    col_idx, row_idx = point
    row = wood[row_idx]
    # print("right: ", row[col_idx + 1 :])
    return row[col_idx + 1 :]

def get_look_up(point):
    col_idx, row_idx = point
    col = [row[col_idx] for row in wood]
    visible_col = col[0:row_idx]
    visible_col.reverse()
    # print("up: ", visible_col)
    return visible_col

def get_look_down(point):
    col_idx, row_idx = point
    col = [row[col_idx] for row in wood]
    # print("down: ", col[row_idx + 1:])
    return col[row_idx + 1:]

def direction_score(list, height):
    for i, item in enumerate(list):
        if item >= height:
            break
    return i + 1
        
        
def scenic_score(point):
    height = tree_map[point]
    ds = direction_score(get_look_down(point), height)
    us = direction_score(get_look_up(point), height)
    ls = direction_score(get_look_left(point), height)
    rs = direction_score(get_look_right(point), height)
    return ds * us * ls * rs
    

def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        wood.append(list(line))
    for row_idx, row in enumerate(wood):
        for col_idx, tree_height in enumerate(row):
            tree_point = (col_idx, row_idx)
            tree_map[tree_point] = tree_height
    for tree in tree_map:
        # edges have scenic score 0
        if not is_edge(tree):
            # calculate score and add to dict
            scenic_scores[tree] = scenic_score(tree)

    return max(scenic_scores.values())


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
