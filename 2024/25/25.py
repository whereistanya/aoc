#!/usr/bin/env python

import sys
import util.grid as gridlib

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

if len(sys.argv) > 1:
  print (sys.argv)

DEBUG = False

locks = []
keys = []
grids = []

gridlines = []
for line in lines:
  if line == "":
    grids.append(gridlib.Grid(gridlines))
    gridlines = []
    continue
  gridlines.append(line)

if gridlines:
  grids.append(gridlib.Grid(gridlines))
  gridlines = []


for grid in grids:
  top_row = grid.get_row(0)
  top_vals = set([x.value for x in top_row])
  bottom_row = grid.get_row(grid.maxy - 1)
  bottom_vals = set([x.value for x in bottom_row])
  if top_vals == {"."} and bottom_vals == {"#"}:
    keys.append(grid)
  elif top_vals == {"#"} and bottom_vals == {"."}:
    locks.append(grid)
  else:
    print("weird grid", grid, top_vals, bottom_vals)
    exit()

lockheights = []
keyheights = []

for lock in locks:
  counts = []
  for x in range(lock.maxx):
    counts.append(-1)
    col = lock.get_col(x)
    for point in col:
      if point.value != "#":
        break
      counts[x] += 1
  lockheights.append(counts)


for key in keys:
  counts = []
  for x in range(key.maxx):
    counts.append(-1)
    col = key.get_col(x)
    for point in reversed(col):
      if point.value != "#":
        break
      counts[x] += 1
  keyheights.append(counts)


part1 = 0
for l in range(len(locks)):
  lock = locks[l]
  lockheight = lockheights[l]
  for k in range(len(keys)):
    key = keys[k]
    keyheight = keyheights[k]

    for col in range(5):
      fit = True
      if lockheight[col] + keyheight[col] > 5:
        fit = False
        break
    if fit:
      print("yes for lock", l, "key", k)
      part1 += 1

print("Part 1:", part1)
