#!/usr/bin/env python3

import functools
import operator

VERBOSE = False
TEST = False

with open("input3.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

example = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.1"""

if TEST:
  lines = example.strip().split("\n")


def has_symbol(x, y):
  neighbors = [ (x - 1, y - 1), (x - 1,   y), (x - 1, y + 1),
                (x    , y - 1),               (x    , y + 1),
                (x + 1, y - 1), (x + 1,   y), (x + 1, y + 1) ]
  stars = []
  symbols = False
  for (nx, ny) in neighbors:
    try:
      char = lines[ny][nx]
    except IndexError: # off the edge of the grid
      continue
    if char.isdigit():
      continue
    if char == ".":
      continue
    symbols = True
    if char == "*":
      stars.append( (nx, ny) )
  return (symbols, stars)

total = 0

for y in range(len(lines)):
  s = ""
  for x in range(len(lines[0])):
    s += lines[y][x]
  print (s)


number = ""
symbol_count = 0
stars_found = set()
all_stars = {}

for y in range(len(lines)):
  for x in range(len(lines[0])):
    char = lines[y][x]

    # if we're reading a number
    if char.isdigit():
      number += char
      symbols, stars = has_symbol(x, y)
      if symbols:
        symbol_count += 1
      if stars:
        stars_found.update(stars)

    # otherwise reset the number
    else:
      if number != "":
        print (number, symbol_count, stars_found)
        if symbol_count > 0:
          total += int(number)
        for star in stars_found:
          try:
            all_stars[star].append(int(number))
          except KeyError:
            all_stars[star] = [int(number)]
      number = ""
      symbol_count = 0
      stars_found.clear()

# Fencepost, gross
if number != "":
  if symbol_count > 0:
    total += int(number)
  for star in stars_found:
    try:
      all_stars[star].append(int(number))
    except KeyError:
      all_stars[star] = [int(number)]
number = ""


print("Part 1:", total)

total_part2 = 0
for v in all_stars.values():
  if len(v) == 2:
    total_part2 += functools.reduce(operator.mul, v)
print("Part 2:", total_part2)
