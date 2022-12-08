from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
wood = []
tree_map = {}

def is_edge(point):
    no_of_cols = len(wood[0])
    no_of_rows = len(wood)
    col_idx, row_idx = point
    if row_idx == 0 or row_idx == no_of_rows-1:
        return True 
    elif col_idx == 0 or col_idx == no_of_cols-1:
        return True
    else:
        return False
    
def row_visibilty(point):
    no_of_cols = len(wood[0])
    col_idx, row_idx = point
    row = wood[row_idx]
    point_height = tree_map[point]
    return not any(row[i] >= point_height for i in range(0, col_idx)) or not any(row[i] >= point_height for i in range(col_idx + 1, no_of_cols))

def col_visibilty(point):
    no_of_rows = len(wood)
    col_idx, row_idx = point
    point_height = tree_map[point]
    return not any(tree_map[(col_idx, i)] >= point_height for i in range(0, row_idx)) or not any(tree_map[(col_idx, i)] >= point_height for i in range(row_idx + 1, no_of_rows))

def is_visible(point):
    if is_edge(point):
        return True
    else:
        # print(f"##### {point} {tree_map[point]} #####")
        # print(f"row: {wood[point[1]]}")
        # print(f"row_visibility: ", row_visibilty(point))
        # print(f"col_visibility: ", col_visibilty(point))
        return row_visibilty(point) or col_visibilty(point)

def compute(s: str) -> int:
    visible_count = 0
    lines = s.splitlines()
    for line in lines:
        wood.append(list(line))
    for row_idx, row in enumerate(wood):
        for col_idx, tree_height in enumerate(row):
            tree_point = (col_idx, row_idx)
            tree_map[tree_point] = tree_height
    print(tree_map)
    for tree in tree_map:
        if is_visible(tree):
            visible_count += 1
    return visible_count


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected
    assert row_visibilty((2,3)) == True
    assert row_visibilty((2,4)) == False



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
