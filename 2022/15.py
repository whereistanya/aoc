#!/usr/bin/env python3

import re

test = False
#test = True

if test:
  filename = "test15.txt"
  part1Row = 10
  minxy = 0
  maxxy = 20
else:
  filename = "input15.txt"
  part1Row = 2000000
  minxy = 0
  maxxy = 4000000

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

class Sensor(object):
  def __init__(self, x, y, bx, by):
    self.x = x
    self.y = y
    self.bx = bx
    self.by = by
    # the radius from the sensor. no beacon is nearer to the sensor than this value
    self.space = abs(bx - x) + abs(by - y)

  def in_sensor_range(self, y):
    ydist = abs(self.y - y)
    remaining = self.space - ydist
    if remaining < 0: # this row is too far away to be in this sensor's diamond
      return 0,0,False

    a = self.x - remaining
    b = self.x + remaining
    return min(a,b), max(a, b), True

sensors = []
beacons = set()

# Parse input. It looks like:
#lines = ["Sensor at x=8, y=7: closest beacon is at x=2, y=10"]
line_re = "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
for line in lines:
  matches = re.finditer(line_re, line)
  for match in matches:
    sx, sy, bx, by = [int(x) for x in match.groups()]
    sensors.append(Sensor(sx, sy, bx, by))
    beacons.add((bx,by))


def findgaps(row, sensors):
  ranges = []
  for s in sensors:
    smin, smax, in_range = s.in_sensor_range(row)
    if not in_range:
      continue
    ranges.append((smin, smax))

  ranges = sorted(ranges) # (minx, maxx) for a given row, y
  gaps = [] # range is inclusive

  start = ranges[0][0]
  end = 0
  index = start

  for rmin, rmax in ranges:
    if index >= rmin and index <= rmax:
      index = rmax + 1
    elif index < rmin:
      gaps.append((index, rmin - 1))
      index = rmax
    if rmax > end:
      end = rmax
    # don't check if it's greater than rmax because we might have gone past the end
    # of rmax and into the next range.
  return gaps, start, end


# Part 1
# Each sensor lists closest beacon, showing where there can't be beacons
gaps, start, end = findgaps(part1Row, sensors)
impossible = end - start
print("Part 1:", impossible)
for rmin, rmax in gaps: # all ranges not covered by sensors
  print("minus %d-%d inclusive" % (rmin, rmax))


# Part2
# Find the only possible position for the distress beacon.
part2 = 0
for row in range(0, maxxy):
  print(row)
  gaps, start, end = findgaps(row, sensors)
  #print(gaps, start, end)
  if gaps:
    print("Found gaps on row %d: %s" % (row, gaps))
    x = gaps[0][0]
    y = row
    print("x=%d, y=%d" % (x, y))
    part2 = x * 4000000 + y
    break

print("Part 2:", part2)
