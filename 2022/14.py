#!/usr/bin/env python3
# Advent of code Day 14.

import math
import sys

with open("input14.txt", "r") as f:
#with open("test14.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]
  groups = [x.split("->") for x in lines]




class Wall(object):
  def __init__(self, x1, y1, x2, y2):

    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2

  def range(self):
    x1 = self.x1
    x2 = self.x2
    y1 = self.y1
    y2 = self.y2

    if self.x1 != self.x2 and self.y1 != self.y2:
      print("BUG: expected a straight line, got %s" % self)
      exit(1)

    spaces = []
    if self.x1 == self.x2:
      x = x1
      low, high = sorted([y1, y2])
      # trying expanding all the ranges upfront
      # might be more efficient to check each range as needed
      for y in range(low, high + 1):
        spaces.append((x, y))
    else:
      y = y1
      low, high = sorted([x1, x2])
      for x in range(low, high + 1):
        spaces.append((x, y))
    return spaces

  def __repr__(self):
    return "[ %d,%d -> %d,%d]" % (self.x1, self.y1, self.x2, self.y2)

class Cave(object):
  def __init__(self):
    self.walls = []
    self.max_x = 0
    self.max_y = 0
    self.min_x = math.inf
    #self.min_y = math.inf
    self.min_y = 0  # TODO: always?
    self.rocks = set()
    self.start = (500, 0)
    self.sand = set()
    self.last_path = set()

  def add_wall(self, wall):
    self.walls.append(wall)
    for x in [wall.x1, wall.x2]:
      if x > self.max_x:
        self.max_x = x
      if x < self.min_x:
        self.min_x = x
    for y in [wall.y1, wall.y2]:
      if y > self.max_y:
        self.max_y = y
      if y < self.min_y:
        self.min_y = y
    # TODO: bet there's a nicer insert
    for rock in wall.range():
      self.rocks.add(rock)

  def print(self):
    for y in range (self.min_y, self.max_y + 1):
      #s = "%d" % y
      s = ""
      for x in range (self.min_x - 1, self.max_x + 1):
        if (x, y) in self.rocks:
          s += "#"
        elif (x, y) == self.start:
          s += "+"
        elif (x, y) in self.last_path:
          s += "~"
        elif (x, y) in self.sand:
          s += "o"
        else:
          s += "."
      print(s)

  def can_drop(self):
    if self.empty(self.start[0], self.start[1]):
      return True
    return False

  def empty(self, x, y):
    #if y > self.max_y:
    #  return False
    if ((x, y) in self.rocks or
       (x, y) in self.sand):
          return False
    return True

  def drop_sand(self):
    """Returns:
        False: in void, stop dropping
        True: fine, keep dropping
    """
    x, y = self.start
    self.last_path = set()
    while True:
      last_pos = (x, y)
      while (self.empty(x, y + 1)):
        if y > self.max_y:
          return False # off the end
        y += 1
        self.last_path.add((x, y))
      if (self.empty(x - 1, y + 1)):
        x -= 1
        y += 1
        self.last_path.add((x, y))
      elif (self.empty(x + 1, y + 1)):
        x += 1
        y += 1
        self.last_path.add((x, y))
      if (x, y) == last_pos:
        break
    self.sand.add((x, y))
    return True


cave = Cave()

for group in groups:
  prev = None
  for position in group:
    x, y = [int(x.strip()) for x in position.split(",")]
    if prev:
      wall = Wall(prev[0], prev[1], x, y)
      cave.add_wall(wall)
    prev = (x, y)

i = 0

while cave.can_drop():
  if not cave.drop_sand():
    break
  i += 1
cave.print()
print("Part 1:", i)

cave.sand = set()
extra_floor = 200
floor = Wall(cave.min_x - extra_floor, cave.max_y + 2,
             cave.max_x + extra_floor, cave.max_y + 2)
cave.add_wall(floor)

i = 0
while cave.can_drop():
  if not cave.drop_sand():
    print("Need more floor after", i)
    break
  i += 1
print("Part 2:", i)

