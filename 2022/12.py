#!/usr/bin/env python3

import collections
import math

visualize = False
filename = "input12.txt"
#filename = "test12.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

grid = {}
start = None
end = None

for y in range(len(lines)):
  line = lines[y]
  for x in range(len(lines[0])):
    grid[(x, y)] = line[x]
    if line[x] == "S":
      if start:
        print("BUG: found start more than once:")
        print(start, "and", (x, y))
        exit(1)
      start = (x, y)
    if line[x] == "E":
      if end:
        print("BUG: found end more than once:")
        print(end, "and", (x, y))
        exit(1)
      end = (x, y)
# Set extra elevations
grid[start] = 'a'
grid[end] = 'z'


def bfs(grid, start, goal, seen):
  to_check = set() #deque()
  seen.add(start)
  steps = 0
  to_check.add(start)
  while to_check:
    if visualize:
      for y in range(len(lines)):
        s = ""
        for x in range(len(lines[0])):
          if (x, y) in seen:
            s += "#"
          else:
            s += "."
        print(s)
      print(steps, ":", len(to_check), "to check")

    this_step = set(to_check)
    to_check.clear()
    for current in this_step:
      seen.add(current)
      if current == goal:
        return steps
      x, y = current
      possible = [(x - 1, y), (x + 1, y), (x, y -1), (x, y + 1)]
      for p in possible:
        if p not in grid:
          continue
        if p in seen:
          continue
        if ord(grid[p]) - ord(grid[current]) > 1:
          continue
        to_check.add(p)
    steps += 1

part1 = bfs(grid, start, end, set())
print("Part 1: found the end in %d steps" % part1)

shortest = math.inf
for k, v in grid.items():
  if v == 'a':
    steps = bfs(grid, k, end, set())
    if steps and steps < shortest:
      shortest = steps
print("Part 2: shortest path is", shortest)

