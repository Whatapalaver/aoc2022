# advent of code 2022

https://adventofcode.com/2022

This setup repo is from anthonywritescode
This is his [video guide](https://www.youtube.com/watch?v=CZZLCeRya74)

## Instructions

### Initial setup

- create a `.env` file with `session=XXXX` - you can get the session key by logging into advent of code and revealing it wiuth the developer tool `Application-Cookies`
- setup virtualenv `python3 -m venv venv`

### Ongoing

- activate with `source venv/bin/activate` unless you've setup aactivator as Anthony recommends
- copy day00 to relevant day `cp -r day00 day01`
- cd to latest day folder
- grab your input text `aoc-download-input`

### Solving problems

- implement your solution in the `def compute` function
- Add the test case and expected result to INPUT_S and EXPECTED respectively
- run test with `pytest part1.py`
- run script with `python3 part1.py input.txt`
- submit your answer with either `echo answer | aoc-submit --part 1` or `python3 part1.py input.txt | aoc-submit --part 1`

- `cp part1.py part2.py` then solve as above
