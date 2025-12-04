#!/usr/bin/env python

import math
import sys
import util.grid as gridlib

filename = "input.txt"
#filename = "test1"
#filename = "test2"

def turndist(current, new):
  opposite = {"north": "south", "east": "west", "south":"north", "west": "east"}
  if current == new:
    return 0
  if current == opposite[new]:
    return 2
  return 1


def bfs(grid, start):
  to_check = [(start, "east", 0, [start])]
  lowest = math.inf
  paths = []
  seen = {} # (position, orientation): lowest score that's been at this point
  while to_check:
    this_step = list(to_check)
    to_check = []
    for current in this_step:
      pos, movementDirection, score, path = current
      seen[(pos, movementDirection)] = score

      if pos.value == "E":
        path.append(pos)
        if score < lowest:
          lowest = score
          paths = [path]
        elif score == lowest:
          paths.append(path)
      if score > lowest:
        continue # abandon this path
      neighbors = grid.neighbours_by_direction(pos, diagonal=False)
      for direction, point in neighbors.items():
        if point is None:
          continue
        if point.value == "#":
          continue
        if (point, direction) in seen and seen[(point, direction)] < score:
          continue
        turncost = turndist(movementDirection, direction)
        nextpath = list(path)
        nextpath.append(pos)
        # Score increases by 1 point for a move, 1000 for each 90 degree turn
        if turncost == 0: # same direction!
          to_check.append((point, direction, score + 1, nextpath))
        elif turncost == 1: # one 90 deg turn in either direction
          to_check.append((point, direction, score + 1001, nextpath))
        elif turncost == 2: # two 90 deg turns
          to_check.append((point, direction, score + 2001, nextpath))
  return lowest, paths

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

grid = gridlib.Grid(lines)
grid.printnocolor()

start = grid.get_by_char("S")[0]
part1, paths = bfs(grid, start)

tiles = set()
for path in paths:
  for point in path:
    tiles.add(point)

part2 = len(tiles)

print("Part 1:", part1)
print("Part 2:", part2)
