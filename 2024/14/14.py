#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"
maxx = 101
maxy = 103

#filename = "test1"
#maxx = 11
#maxy = 7

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def move(x, y, dx, dy, count):
  x += dx * count
  x = x % maxx
  y += dy * count
  y = y % maxy
  return x, y

def countQuadrants(positions):
  count1 = 0
  count2 = 0
  count3 = 0
  count4 = 0
  midx = int((maxx - 1) / 2)
  midy = int((maxy - 1) / 2)
  for px, py, _, _ in positions:
    if px == midx or py == midy:
      continue

    if px < midx and py < midy:
      count1 += 1
    elif px < midx and py > midy:
      count2 += 1
    elif px > midx and py < midy:
      count3 += 1
    elif px > midx and py > midy:
      count4 += 1
  return count1 * count2 * count3 * count4

gridlines = []
for y in range(maxy):
  s = "." * maxx
  gridlines.append(s)
grid = gridlib.Grid(gridlines)
grid.printgrid()

part1 = 0
part2 = 0

robots = []
for line in lines:
  pos, vel = line.split()
  px, py = [int(x) for x in pos.split("=")[1].split(",")]
  dx, dy = [int(x) for x in vel.split("=")[1].split(",")]
  robots.append((px, py, dx, dy))


nextpos = []
i = 1

midx = int((maxx - 1) / 2)
midy = int((maxy - 1) / 2)

while True:
  nextpos = []
  mid1 = False
  mid2 = False
  mid3 = False
  for robot in robots:
    px, py, dx, dy = robot
    x, y = move(px, py, dx, dy, 1)
    grid.setvalue(x, y, "1")
    nextpos.append((x, y, dx, dy))
    if x == midx and y == midy:
      mid1 = True
    if x == midx - 1 and y == midy:
      mid2 = True
    if x == midx + 1 and y == midy:
      mid3 = True

  if i == 100:
    part1 = countQuadrants(nextpos)
    print("Part 1", part1)
  robots = nextpos

  if mid1 and mid2 and mid3:
    grid.printgrid()
    print("If this is a christmas tree, part 2 is", i)
    _ = input("Otherwise, press enter to continue")
  i += 1
  for p in grid.grid.values():
    p.value = "."

print("Part 1:", part1)
print("Part 2:", part2)
