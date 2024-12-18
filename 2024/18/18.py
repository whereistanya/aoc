#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib


# a two-dimensional grid with coordinates that range from 0 to 70 both
# horizontally and vertically.
filename = "input.txt"
maxx = 70 # 0 to 70
maxy = 70
out = (70, 60)
first = 1024

# test
"""
filename = "test1"
maxx = 6
maxy = 6
out = (6, 6)
first = 12
#"""

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


part1 = 0
part2 = 0

gridlines = []
for i in range(maxx + 1):
  gridlines.append( "." * (maxx + 1))
print(gridlines)

grid = gridlib.Grid(gridlines) 

for line in lines[0:first]:
  x, y = [int(x) for x in line.strip().split(",")]
  grid.setvalue(x, y, "#")

corrupted = grid.get_by_char("#")
grid.printnocolor()
print(len(corrupted), "bad blocks")

start = grid.getpoint_from_xy(0, 0)

def shortest_path(grid, start):
  to_check = set([start])
  visited = set()
  count = 0

  while to_check:
    this_round = list(to_check)
    for p in this_round:
      grid.setvalue(p.x, p.y, "O")
    #print(count, ":", this_round)
    #grid.printnocolor()
    to_check = set()
    for p in this_round:
      visited.add(p)
      if p.x == maxx and p.y == maxy:
        return count
      neighbours = p.neighbours(diagonal=False)
      for n in neighbours:
        if n in visited:
          continue
        if n is None:
          continue
        if n.value == "#":
          continue
        to_check.add(n)
    count += 1
  print("No path")
  return -1

part1 = shortest_path(grid, start)

for i in range(first, len(lines)):
  line = lines[i]
  print("trying", line)
  x, y = [int(x) for x in line.strip().split(",")]
  grid.setvalue(x, y, "#")
  shortest = shortest_path(grid, start)
  if shortest == -1:
    part2 = lines[i]
    break


print("Part 1:", part1)
print("Part 2:", part2)
