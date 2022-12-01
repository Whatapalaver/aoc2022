from __future__ import annotations
from collections import Counter, defaultdict, namedtuple, deque
from itertools   import permutations, combinations, chain, cycle, product, islice
from heapq       import heappop, heappush

import argparse
import contextlib
import enum
import math
import os.path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Generator
import ssl
import certifi



HERE = os.path.dirname(os.path.abspath(__file__))


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}', file=sys.stderr, flush=True)


def _get_cookie_headers() -> dict[str, str]:
    with open(os.path.join(HERE, '../.env')) as f:
        contents = f.read().strip()
    return {'Cookie': contents}


def get_input(year: int, day: int) -> str:
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = urllib.request.Request(url, headers=_get_cookie_headers())
    return urllib.request.urlopen(req, context=ssl.create_default_context(cafile=certifi.where())).read().decode()


def get_year_day() -> tuple[int, int]:
    cwd = os.getcwd()
    day_s = os.path.basename(cwd)
    year_s = os.path.basename(os.path.dirname(cwd))

    if not day_s.startswith('day') or not year_s.startswith('aoc'):
        raise AssertionError(f'unexpected working dir: {cwd}')

    return int(year_s[len('aoc'):]), int(day_s[len('day'):])


def download_input() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    year, day = get_year_day()

    for i in range(5):
        try:
            s = get_input(year, day)
        except urllib.error.URLError as e:
            print(f'zzz: not ready yet: {e}')
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit('timed out after attempting many times')

    with open('input.txt', 'w') as f:
        f.write(s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print('...')
    else:
        print(lines[0][:80])
        print('...')

    return 0


TOO_QUICK = re.compile('You gave an answer too recently.*to wait.')
WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


def _post_answer(year: int, day: int, part: int, answer: int) -> str:
    params = urllib.parse.urlencode({'level': part, 'answer': answer})
    req = urllib.request.Request(
        f'https://adventofcode.com/{year}/day/{day}/answer',
        method='POST',
        data=params.encode(),
        headers=_get_cookie_headers(),
    )
    resp = urllib.request.urlopen(req, context=ssl.create_default_context(cafile=certifi.where()))

    return resp.read().decode()


def submit_solution() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', type=int, required=True)
    args = parser.parse_args()

    year, day = get_year_day()
    answer = int(sys.stdin.read())

    print(f'answer: {answer}')

    contents = _post_answer(year, day, args.part, answer)

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f'\033[41m{error_match[0]}\033[m')
            return 1

    if RIGHT in contents:
        print(f'\033[42m{RIGHT}\033[m')
        return 0
    else:
        # unexpected output?
        print(contents)
        return 1


def submit_25_pt2() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    year, day = get_year_day()

    assert day == 25, day
    contents = _post_answer(year, day, part=2, answer=0)

    if 'Congratulations!' in contents:
        print('\033[42mCongratulations!\033[m')
        return 0
    else:
        print(contents)
        return 1


def adjacent_4(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y


def adjacent_8(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for y_d in (-1, 0, 1):
        for x_d in (-1, 0, 1):
            if y_d == x_d == 0:
                continue
            yield x + x_d, y + y_d


def parse_coords_int(s: str) -> dict[tuple[int, int], int]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = int(c)
    return coords


def parse_coords_hash(s: str) -> set[tuple[int, int]]:
    coords = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                coords.add((x, y))
    return coords


def parse_numbers_split(s: str) -> list[int]:
    return [int(x) for x in s.split()]


def parse_numbers_comma(s: str) -> list[int]:
    return [int(x) for x in s.strip().split(',')]


def format_coords_hash(coords: set[tuple[int, int]]) -> str:
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)
    return '\n'.join(
        ''.join(
            '#' if (x, y) in coords else ' '
            for x in range(min_x, max_x + 1)
        )
        for y in range(min_y, max_y + 1)
    )


def print_coords_hash(coords: set[tuple[int, int]]) -> None:
    print(format_coords_hash(coords))


class Direction4(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    @property
    def _vals(self) -> tuple[Direction4, ...]:
        return tuple(type(self).__members__.values())

    @property
    def cw(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) + 1) % len(vals)]

    @property
    def ccw(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) - 1) % len(vals)]

    @property
    def opposite(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) + 2) % len(vals)]

    def apply(self, x: int, y: int, *, n: int = 1) -> tuple[int, int]:
        return self.x * n + x, self.y * n + y


# Include utilities from Peter Norvig
# https://nbviewer.org/url/norvig.com/ipython/Advent%20of%20Code.ipynb

# Examples

# assert tuple(transpose(((1, 2, 3), (4, 5, 6)))) == ((1, 4), (2, 5), (3, 6))
# assert first('abc') == first(['a', 'b', 'c']) == 'a'
# assert cat(['a', 'b', 'c']) == 'abc'
# assert (groupby(['test', 'one', 'two', 'three', 'four'], key=len) == {3: ['one', 'two'], 4: ['test', 'four'], 5: ['three']})

def transpose(matrix): return zip(*matrix)

def first(iterable): return next(iter(iterable))

def nth(iterable, n, default=None):
    "Returns the nth item of iterable, or a default value"
    return next(islice(iterable, n, None), default)

def grep(pattern, lines):
    "Print lines that match pattern."
    for line in lines:
        if re.search(pattern, line):
            print(line)

def groupby(iterable, key=lambda it: it):
    "Return a dic whose keys are key(it) and whose values are all the elements of iterable with that key."
    dic = defaultdict(list)
    for it in iterable:
        dic[key(it)].append(it)
    return dic

def powerset(iterable):
    "Yield all subsets of items."
    items = list(iterable)
    for r in range(len(items)+1):
        for c in combinations(items, r):
            yield c

# 2-D points implemented using (x, y) tuples
def X(point): return point[0]
def Y(point): return point[1]

def neighbors4(point): 
    "The four neighbors (without diagonals)."
    x, y = point
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))

def neighbors8(point): 
    "The eight neighbors (with diagonals)."
    x, y = point 
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (X+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1))

def cityblock_distance(p, q=(0, 0)): 
    "City block distance between two points."
    return abs(X(p) - X(q)) + abs(Y(p) - Y(q))

def euclidean_distance(p, q=(0, 0)): 
    "Euclidean (hypotenuse) distance between two points."
    return math.hypot(X(p) - X(q), Y(p) - Y(q))

def trace1(f):
    "Print a trace of the input and output of a function on one line."
    def traced_f(*args):
        result = f(*args)
        print('{}({}) = {}'.format(f.__name__, ', '.join(map(str, args)), result))
        return result
    return traced_f

def astar_search(start, h_func, moves_func):
    "Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0)."
    frontier  = [(h_func(start), start)] # A priority queue, ordered by path length, f = g + h
    previous  = {start: None}  # start state has no previous state; other states will
    path_cost = {start: 0}     # The cost of the best path to a state.
    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))
                
def Path(previous, s): 
    "Return a list of states that lead to state s, according to the previous dict."
    return ([] if (s is None) else Path(previous, previous[s]) + [s])
