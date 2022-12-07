from __future__ import annotations
from collections import defaultdict

import argparse
import os.path
import re
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
DISK_SIZE = 70000000
REQUIRED = 30000000


current_path_items = []

immediate_dir_size = defaultdict(lambda: 0)

dir_total_size = defaultdict(lambda: 0)

def part_2_result(totals_dict):
    
    existing_size = totals_dict['/']
    additional_required = REQUIRED - (DISK_SIZE - existing_size)
    print("reqd: ", additional_required)
    sorted_total_dict = {k: v for k, v in sorted(totals_dict.items(), key=lambda path: path[1])}
    print("totals: ", sorted_total_dict)
    for path in sorted_total_dict:
        if sorted_total_dict[path] >= additional_required:
            return sorted_total_dict[path]

def part_1_result(totals_dict):
    result = 0
    for path in totals_dict.keys():
        size = totals_dict[path]
        if  size <= 100000:
            result += size
    return result
            

def generate_total_size_dict():
    dir_total_size = defaultdict(lambda: 0, immediate_dir_size)
    for initial_path in immediate_dir_size.keys():
        for path in immediate_dir_size.keys():
            if path.startswith(initial_path) and path != initial_path:
                dir_total_size[initial_path] += immediate_dir_size[path]

    return dir_total_size
    

def current_working_path():
    """returns current working path"""
    path = ''.join(current_path_items[1:])
    if len(path) == 0:
        return '/'
    else:
        new_path = re.sub(r'$\//', '/', path)   
        return f"{new_path}/"

def compute(s: str) -> int:
    lines = s.splitlines()
    list_mode = False
    for line in lines:
        if list_mode and not line.startswith('$'):
            cwp = current_working_path()
            # add cwp to immediate_dir_size dict (initialised at size 0 with defaultdict)
            immediate_dir_size[cwp] += 0
            if line.startswith('dir'):
                _, dir = line.split(" ")
                # add new dir to immediate_dir_size dict (initialised at size 0 with defaultdict)
                immediate_dir_size[f"{cwp}{dir}/"] += 0
            else:
                file_size, filename = line.split(" ")
                immediate_dir_size[cwp] += int(file_size)
        # check for command mode
        if line.startswith('$'):
            list_mode = False
            if line.startswith('$ ls'):
                # re-enter list mode
                list_mode = True
            elif line.startswith('$ cd ..'):
                current_path_items.pop()
            elif line.startswith('$ cd'):
                _, _, dir = line.split(" ")
                if dir == "/":
                    current_path_items.append(dir)
                else:
                    current_path_items.append(f"/{dir}")
                # print("cwp_items: ",current_path_items)  
    totals = generate_total_size_dict()
    return part_2_result(totals)
            


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


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
