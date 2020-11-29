#!/usr/bin/env python
# Advent of code Day 17.

import re
import sys

line_re = "(\w)=(\d+), (\w)=(\d+)..(\d+)"

class Ground(object):
  def __init__(self):
    self.clay = set()
    self.bottom = 0  # down is higher numbers
    self.top = 10000000
    self.water = set()
    self.falling_water = set()
    self.readfile()

  def readfile(self):
    with open("day17input.txt", "r") as f:
      lines = f.readlines()

    """
    lines = [
      "x=495, y=2..7",
      "y=7, x=495..501",
      "x=501, y=3..7",
      "x=498, y=2..4",
      "x=506, y=1..2",
      "x=498, y=10..13",
      "x=504, y=10..13",
      "y=13, x=498..504",
    ]
 #   """

    for line in lines:
      groups = re.search(line_re, line).groups()
      if len(groups) != 5:
        print("Bad input [%s] matched [%s]" % (line, groups))
        sys.exit(1)
      for i in range(int(groups[3]), int(groups[4]) + 1):
        if groups[2] == "x":
          assert groups[0] == "y"
          x = i
          y = int(groups[1])
        else:
          assert groups[0] == "x"
          assert groups[2] == "y"
          x = int(groups[1])
          y = i
        self.clay.add((x, y))
        if y > self.bottom:
          self.bottom = y
        if y < self.top:
          self.top = y

  def draw(self):
    for y in range(0, self.bottom + 1):
      s = "%03d" % y
      for x in range(350, 600):
        if (x, y) == (500, 0):
          s += "+"
        elif (x, y) in ground.clay:
          s += "#"
        elif (x, y) in ground.water:
          s += "~"
        elif (x, y) in ground.falling_water:
          s += "|"
        else:
          s += "."
      print(s)
    print("===============\n")


  def occupied(self, coord):
    """Return whether there's something (clay, water) in this square.
    Args:
        coord: (x, y): x, y tuple
    """
    x, y =coord
    if (x, y) in self.clay or (x, y) in self.water:
      return True
    return False

  def find_shelf(self, x, y):
    """
    Given an x,y coordinate, C, this returns A and B like this:
    #A    C           B#
    ####################
    Returns min_y, max_x of shelf, 
    or min_x, None, or None, max_x if only one side is bounded
    or None, None if neither side is

    None if it isn't one.
    Returns coordinates where water can sit, not the actual wall.
    """
    if (x, y) in self.clay:
      return None, None
    min_x = x
    while min_x > 0:
      if not self.occupied((min_x, y+1)):
        min_x = None
        break
      if (min_x - 1 , y) in self.clay:
        break
      min_x = min_x - 1

    # now we have min_x or we've returned
    max_x = x
    while True:  # bound this if you're fancy
      if not self.occupied((max_x, y + 1)):
        max_x = None
        break

      if (max_x + 1, y) in self.clay:
        break
      max_x = max_x + 1
    return (min_x, max_x)

# Main.

ground = Ground()

water_rest = set()
water_transit = set()

starting_points = [(500, 1)]

while starting_points:
  x, y = starting_points.pop()
  while True:

# if there's nothing under this space, go straight down
    if not ground.occupied((x, y + 1)):
      if y > ground.bottom:
        break
      if y >= ground.top:
        ground.falling_water.add((x, y))

      # if we would hit falling water, this path's already been done
      if (x, y + 1) in ground.falling_water:
        break

      y = y + 1
      continue

    else: # ground below is occupied. Start pooling water.
      shelf = ground.find_shelf(x, y)
      min_x, max_x = shelf

      if min_x and max_x:
# it's an actual shelf
        for water_x in range(min_x, max_x + 1):
          ground.water.add((water_x, y))
        y = y - 1
        continue

# it's bounded on one side and should spill over
      elif min_x:
          for water_x in range(min_x, x + 1):
            ground.falling_water.add((water_x, y))
          x = x + 1
          continue

      elif max_x:
          for water_x in range(x, max_x + 1):
            ground.falling_water.add((water_x, y))
          x = x - 1
          continue

# it's bounded no sides. Save one location for later and go the other way.
      else:
        ground.falling_water.add((x, y))
        min_x = x
        while ground.occupied((min_x - 1, y + 1)):
          ground.falling_water.add((min_x - 1, y))
          min_x -= 1
        starting_points.append((min_x - 1, y))
        max_x = x
        while ground.occupied((max_x + 1, y + 1)):
          ground.falling_water.add((max_x + 1, y))
          max_x += 1

        x = max_x + 1
        continue

ground.draw()

print("At rest", len(ground.water))
print("In motion", len(ground.falling_water))
print("Water", len(ground.water.union(ground.falling_water)))

