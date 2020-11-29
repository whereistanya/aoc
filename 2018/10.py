#!/usr/bin/env python
# Advent of code Day 1.

import os
import re

class Point(object):
  def __init__(self, x, y, deltax, deltay):
    self.x = x
    self.y = y
    self.deltax = deltax
    self.deltay = deltay

line_re = "position=<\s*(-?\d+),\s*(-?\d+)>\s*velocity=<\s*(-?\d+),\s*(-?\d+)>"

with open("day10input.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
	"position=< 9,  1> velocity=< 0,  2>",
	"position=< 7,  0> velocity=<-1,  0>",
	"position=< 3, -2> velocity=<-1,  1>",
	"position=< 6, 10> velocity=<-2, -1>",
	"position=< 2, -4> velocity=< 2,  2>",
	"position=<-6, 10> velocity=< 2, -2>",
	"position=< 1,  8> velocity=< 1, -1>",
	"position=< 1,  7> velocity=< 1,  0>",
	"position=<-3, 11> velocity=< 1, -2>",
	"position=< 7,  6> velocity=<-1, -1>",
	"position=<-2,  3> velocity=< 1,  0>",
	"position=<-4,  3> velocity=< 2,  0>",
	"position=<10, -3> velocity=<-1,  1>",
	"position=< 5, 11> velocity=< 1, -2>",
	"position=< 4,  7> velocity=< 0, -1>",
	"position=< 8, -2> velocity=< 0,  1>",
	"position=<15,  0> velocity=<-2,  0>",
	"position=< 1,  6> velocity=< 1,  0>",
	"position=< 8,  9> velocity=< 0, -1>",
	"position=< 3,  3> velocity=<-1,  1>",
	"position=< 0,  5> velocity=< 0, -1>",
	"position=<-2,  2> velocity=< 2,  0>",
	"position=< 5, -2> velocity=< 1,  2>",
	"position=< 1,  4> velocity=< 2,  1>",
	"position=<-2,  7> velocity=< 2, -2>",
	"position=< 3,  6> velocity=<-1, -1>",
	"position=< 5,  0> velocity=< 1,  0>",
	"position=<-6,  0> velocity=< 2,  0>",
	"position=< 5,  9> velocity=< 1, -2>",
	"position=<14,  7> velocity=<-2,  0>",
	"position=<-3,  6> velocity=< 2, -1>",
]
"""

points = []  # Point

max_x = 0
min_x = 99999

for line in lines:

  groups = re.search(line_re, line).groups()
  if len(groups) != 4:
    print("Bad input [%s] matched [%s]" % (line, groups))
    sys.exit(1)
  x = int(groups[0])
  y = int(groups[1])
  deltax = int(groups[2])
  deltay = int(groups[3])
  points.append(Point(x, y, deltax, deltay))

smallest_width = 9999999

current = set()  # (x, y) tuples

seconds = 0
while True:
  max_x = 0
  max_y = 0
  min_x = 99999
  min_y = 99999
  new_points = set() # (x, y) tuples
  for point in points:
    point.x = point.x + point.deltax
    point.y = point.y + point.deltay
    new_points.add((point.x, point.y))
    if point.x > max_x:
      max_x = point.x
    if point.x < min_x:
      min_x = point.x
    if point.y > max_y:
      max_y = point.y
    if point.y < min_y:
      min_y = point.y
  distance = max_x - min_x
  if distance < smallest_width:
    smallest_width = distance
    current = new_points
    seconds += 1
  else:
    s = ""

    for y in range (min_y, max_y):
      s += "\n"
      for x in range (min_x, max_x):
        if (x, y) in current:
          s += "#"
        else:
          s += "."
    os.system('clear')
    print("After %d seconds..." % seconds) # 10887 is too high.
    print(s)
    break



