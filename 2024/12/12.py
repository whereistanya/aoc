#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib
import collections

filename = "input.txt"
#filename = "test5"


with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


def countCorners(point, grid):
  corners = 0
  nabes = grid.neighbours_by_direction(point)
  vals = {}
  for k, v in nabes.items():
    if v is None:
      vals[k] = -1
    else:
      vals[k] = v.value

  pv = point.value
  groups = [
    ("west", "northwest", "north"),
    ("north", "northeast", "east"),
    ("east", "southeast", "south"),
    ("south", "southwest", "west")
  ]
  for group in groups:
    d1, d2, d3 = group

    if vals[d1] != pv and vals[d2] != pv and vals[d3] != pv:
      corners += 1
    if vals[d1] == pv and vals[d2] != pv and vals[d3] == pv:
      corners += 1
    if vals[d1] != pv and vals[d2] == pv and vals[d3] != pv:
      corners += 1
  return corners

def mapRegion(start, grid, seen):
  to_check = collections.deque([start])
  area = 0
  perimeter = 0
  corners = 0

  while to_check:
    point = to_check.popleft()
    if point in seen:
      continue
    seen.add(point)
    nabes = grid.neighbours(point, diagonal=False)
    perimeter += (4 - len(nabes)) # how many edges
    area += 1
    sameValueNabes = []
    for nabe in nabes:
      if nabe.value != point.value:
        perimeter += 1  # border with other type of plant
      else:
        sameValueNabes.append(nabe)
        if nabe not in seen:
          to_check.append(nabe)
    corners += countCorners(point, grid)

  price1 = area * perimeter
  #print("Region", start.value, "with price", area, "*", perimeter, "=", price1)
  price2 = area * corners
  #print("Part 2:", corners, "corners, so price", price2)

  return price1, price2


part1 = 0
part2 = 0
grid = gridlib.Grid(lines)

seen = set()

for point in grid.grid.values():
  if point in seen:
    continue
  price1, price2 = mapRegion(point, grid, seen)
  part1 += price1
  part2 += price2

grid.printgrid()

print("Part 1:", part1)
print("Part 2:", part2)
