#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

patterns = [x.strip() for x in lines[0].strip().split(",")]
designs = lines[2:]


def makePattern(design, patterns, counts):
  if design == "":
    return 1
  if design in counts:
    return counts[design]
  countPossible = 0
  for pattern in patterns:
    if design.startswith(pattern):
      countPossible += makePattern(design[len(pattern):], patterns, counts)
  counts[design] = countPossible
  return countPossible

part1 = 0
part2 = 0


counts = {}

for design in designs:
  possible = makePattern(design, patterns, counts)
  if possible > 0:
    part1 += 1
    part2 += possible


print("Part 1:", part1)
print("Part 2:", part2)
