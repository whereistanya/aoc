#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"
#filename = "test1"
#filename = "test2"
#filename = "test3"
#filename = "test4"
#filename = "test5"


with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


part1 = 0
part2 = 0

grid = gridlib.Grid(lines)
grid.printgrid()

antennas = []
for point in grid.grid.values():
  if point.value != ".":
    antennas.append(point)

antinodes = set()

for i in antennas:
  for j in antennas:
    if i == j:
      continue
    if i.value != j.value:
      continue
    distx = i.x - j.x
    disty = i.y - j.y

    for xy in [ (i.x - distx, i.y - disty), (i.x + distx, i.y + disty),
      (j.x - distx, j.y - disty), (j.x + distx, j.y + disty)
    ]:
      antinode = grid.getpoint_from_xy(xy[0], xy[1])
      if antinode is not None and antinode != i and antinode != j:
          antinodes.add((xy[0], xy[1]))

part1 = len(antinodes)

print("Part 1:", part1)

# Part2

# all antennas are antinodes in part 2
antinodes = set(antennas)

for i in antennas:
  for j in antennas:
    if i == j:
      continue
    if i.value != j.value:
      continue

    distx = i.x - j.x
    disty = i.y - j.y

    for mul in range (0, 100):
      found = False
      for xy in [
        (i.x - (distx * mul), i.y - (disty * mul)), (i.x + (distx * mul), i.y + (disty * mul)),
        (j.x - (distx * mul), j.y - (disty * mul)), (j.x + (distx * mul), j.y + (disty * mul))
      ]:
        antinode = grid.getpoint_from_xy(xy[0], xy[1])
        if antinode is not None and antinode != i and antinode != j:
          found = True
          antinodes.add(antinode)
        if not found:
          break

for antinode in antinodes:
  grid.setvalue(antinode.x, antinode.y, "#")
grid.printgrid()

part2 = len(antinodes)
print("Part 2:", part2)
