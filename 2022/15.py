#!/usr/bin/env python3

import math
import re

test = True
test = False

if test:
  filename = "test15.txt"
else:
  filename = "input15.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

empty = set()
sensors = set()
beacons = set()
empty_range = {}

def closer(point, start, max_distance):
  "Return True if point is within distance of start, False otherwise"
  sx, sy = start
  px, py = point
  x_dist = abs(sx - px)
  y_dist = abs(sy - py)
  dist = x_dist + y_dist
  # TODO: which branch is = on?
  if dist <= max_distance:
    return True
  else:
    return False

min_x = math.inf
max_x = -math.inf

line_re = "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
for line in lines:
  matches = re.finditer(line_re, line)
  for match in matches:
    sx, sy, bx, by = [int(x) for x in match.groups()]
    sensors.add((sx, sy))
    beacons.add((bx, by))
# Uncomment these lines to only draw empty space for sensor 8,7
# like in the example, to compare pictures.
#lines = ["Sensor at x=8, y=7: closest beacon is at x=2, y=10"]
#for line in lines:
#  matches = re.finditer(line_re, line)
#  for match in matches:
#    sx, sy, bx, by = [int(x) for x in match.groups()]

    x_dist = abs(sx - bx)
    y_dist = abs(sy - by)
    dist = x_dist + y_dist
    print (line)
    print(sx, sy, bx, by, dist)
    if (sx - dist) < min_x:
      min_x = (sx - dist)
    if (sx + dist) > max_x:
      max_x = (sx + dist)
    empty_range[(sx, sy)] = dist

    """for x in range(dist + 1):
      for y in range(0, (dist - x + 1)):
        empty.add((sx + x, sy + y))
        empty.add((sx - x, sy + y))
        empty.add((sx + x, sy - y))
        empty.add((sx - x, sy - y))
print("  --          1111111111122222")
print("  2101234567890123456789012345")
for y in range (-2, 23):
  s = str(y).zfill(2)
  for x in range (-2, 26):
    if (x, y) in sensors:
      s += "S"
    elif (x, y) in beacons:
      s += "B"
    elif (x, y) in empty:
      s += "#"
    else:
      s += "."
  print (s)
"""

"""
# Part 1
print ("Looking from %d to %d" % (min_x, max_x))
count = 0


if test:
  row = 10
else:
  row = 2000000
min_y = row
max_y = row
for y in range(min_y, max_y + 1):
  for x in range (min_x, max_x + 1):
    if (x, y) in beacons:
      continue
    for sensor in sensors:
      if closer((x, y), sensor, empty_range[sensor]):
        count += 1
        break
print("Part 1", count)

exit(0)
"""

# Part 2
min_x = 0
min_y = 0

if test:
  max_x = 20
  max_y = 20
else:
  max_x = 4000000
  max_y = 4000000

print ("Looking from %d to %d" % (min_x, max_x))
for y in range(min_y, max_y + 1):
  print(y)
  for x in range (min_x, max_x + 1):
    if (x, y) in beacons:
      continue
    if (x, y) in sensors:
      continue
    found = False
    for sensor in sensors:
      if closer((x, y), sensor, empty_range[sensor]):
        found = True
        break
    if not found:
      print("%d,%d is possible!" % (x, y))
      print("Freq", (x * 4000000 + y))
      exit(0)

