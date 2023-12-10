#!/usr/bin/env python3

import math
import re

VERBOSE = True
TEST = True
TEST = False

with open("input8.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

example = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

if TEST:
  lines = example.strip().split("\n")

paths = {}  # str: (str, str)
path_re = "^(...) = \((...), (...)\)$"

directions = lines[0]
starts = []

for line in lines[2:]:
  match = re.match(path_re, line)
  origin = match.groups(1)[0]
  path1 = match.groups(1)[1]
  path2 = match.groups(1)[2]
  paths[origin] = (path1, path2)
  if origin.endswith('A'):
    starts.append(origin)

# Part 1
count = 0
current = "AAA"
i = 0
while True:
  i = i % len(directions)
  c = directions[i]
  if c == 'L':
    current = paths[current][0]
  elif c == "R":
    current = paths[current][1]
  count += 1
  if current == "ZZZ":
    break
  i += 1

print("Part 1:", count)

counts = []
for start in starts:
  i = 0
  count = 0
  while True:
    i = i % len(directions)
    c = directions[i]
    if c == 'L':
      start = paths[start][0]
    elif c == 'R':
      start = paths[start][1]
    else:
      print("BUG")
      exit(1)
    count += 1
    if start.endswith("Z"):
      break
    i += 1
  counts.append(count)

print("Part 2:", math.lcm(*counts))
