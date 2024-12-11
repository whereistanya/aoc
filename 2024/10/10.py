#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

grid = gridlib.Grid(lines)

part1 = 0
part2 = 0

trailheads = grid.get_by_char("0")

for th in trailheads:
  to_try = th.neighbours(diagonal=False) 
  seen = set()
  height = 0
  while (to_try):
    to_try_next = []
    for step in to_try:
      if step.value == ".":
        continue
      value = int(step.value)
      if value != height + 1:
        continue
      if value == 9:
        part2 += 1
        if step not in seen:
          part1 += 1
        seen.add(step)
        continue
      # this path is valid, so list where we can go from here
      neighbours = step.neighbours(diagonal=False)
      to_try_next.extend(neighbours)
    height += 1
    to_try = list(to_try_next)


print("Part 1:", part1)
print("Part 2:", part2)
