#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib
import math

test = True
test = False

filename = "input.txt"
minSave = 99

if test:
  filename = "test1"
  minSave = 0


with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


def reachable(grid, p, n):
  points = []
  minx = p.x - n
  maxx = p.x + n + 1

  # xdistance + ydistance can add up to a max of n
  for x in range(minx, maxx):
    xdist = abs(p.x - x)
    ydist = n - xdist
    miny = p.y - ydist
    maxy = p.y + ydist + 1
    for y in range(miny, maxy):
      if x == p.x and y == p.y:
        continue
      point = grid.getpoint_from_xy(x, y)
      if point is None:
        continue
      if point.value == "#":
        continue
      points.append(point)
  return points



def walk(grid, start, cheatTime):
  nextStep = start
  cheats = set()
  savings = {}

  i = 0
  positions = {}
  while nextStep is not None:
    pos = nextStep
    nextStep = None
    positions[pos] = i

    neighbors = grid.neighbours_by_direction(pos, diagonal=False)
    for direction, point in neighbors.items():
      if point is None:
        continue
      if point in positions.keys(): # don't backtrack
        continue
      if point.value in [".", "E"]:
        nextStep = point

    could_reach = reachable(grid, pos, cheatTime)
    for jumpTo in could_reach:
      if jumpTo in positions.keys():
        howLong = i - positions[jumpTo] # when we were there
        movesAway = abs(jumpTo.x - pos.x) + abs(jumpTo.y - pos.y) # cost of shortcut
        possibleSavings = howLong - movesAway
        if possibleSavings > 0:
          cheats.add( (jumpTo, pos) )
          try:
            savings[possibleSavings] += 1
          except KeyError:
            savings[possibleSavings] = 1
    i += 1
  return cheats, savings


grid = gridlib.Grid(lines)

start = grid.get_by_char("S")[0]
end = grid.get_by_char("E")[0]

part1 = 0
cheats, savings = walk(grid, start, 2)
for k, v in sorted(savings.items()):
  if k > minSave:
    #print("There are %d ways to save %d" % (v, k))
    part1 += v

part2 = 0

cheats, savings = walk(grid, start, 20)


for k, v in sorted(savings.items()):
  if k > minSave:
    #print("There are %d ways to save %d" % (v, k))
    part2 += v

print("Part 1:", part1)
print("Part 2:", part2)
