#!/usr/bin/env python

import sys
import util.grid as gridlib

filename = "input11.txt"
#filename = "test11.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

grid = gridlib.Grid(lines)

# any rows or columns that contain no galaxies should all be bigger.
# First find places with extra rows
addrows = []
addcols = []

for i in range(len(lines)):
  line = lines[i]
  chars = set([x for x in line])
  if not "#" in chars:
    addrows.append(i)

# Now find places with extra cols
for x in range(grid.maxx):
  col = grid.get_col(x)
  vals = set([p.value for p in col])
  if not "#" in vals:
    addcols.append(x)

galaxies = grid.get_by_char("#")

part1replacement = 2
#part2replacement = 100 # test data
part2replacement = 1000000


part1dists = []
part2dists = []
for i in range(len(galaxies)):
  for j in range(i + 1, len(galaxies)):
    g1 = galaxies[i]
    g2 = galaxies[j]
    part1dist = abs(g1.x - g2.x) + abs(g1.y - g2.y)
    part2dist = part1dist
    for row in addrows:
      if (row < g1.y and row > g2.y) or (row > g1.y and row < g2.y):
        part1dist += (part1replacement - 1)
        part2dist += (part2replacement - 1)
    for col in addcols:
      if (col < g1.x and col > g2.x) or (col > g1.x and col < g2.x):
        part1dist +=(part1replacement - 1)
        part2dist +=(part2replacement - 1)
    part1dists.append(part1dist)
    part2dists.append(part2dist)

part1 = sum(part1dists)

part2 = sum(part2dists)

print("Part 1:", part1)
print("Part 2:", part2)
