#!/usr/bin/env python
# Advent of code Day 22

import sys



class Region(object):
  def __init__(self, x, y, depth):
    self.x = x
    self.y = y
    self.depth = depth
    self._region_type = "?"
    self._erosion_level = -1
    self._geologic_index = -1
    self.xminus1 = None # neighbour
    self.yminus1 = None # neighbour

  def region_type(self):
    if self._region_type == "?":
      self.erosion_level()
    return self._region_type

  def geologic_index(self):
    if self._geologic_index > 0:
      return self._geologic_index
    if self.y == 0:
      self._geologic_index = self.x * 16807
    elif self.x == 0:
      self._geologic_index = self.y * 48271
    else:
      self._geologic_index = self.xminus1.erosion_level() * self.yminus1.erosion_level()
    return self._geologic_index

  def erosion_level(self):
    if self._erosion_level > 0:
      return self._erosion_level
    self._erosion_level = (self.geologic_index() + self.depth) % 20183
    level = self._erosion_level % 3
    if level == 0:
      self._region_type = "."  # rocky
    elif level == 1:
      self._region_type = "="  # wet
    elif level == 2:
      self._region_type = "|"  # narrow
    else:
      print "Unexpected erosion level:", self._erosion_level
      sys.exit(1)
      return self._erosion_level


class Cave(object):
  def __init__(self, depth, target):
    self.regions = {}  # ((x,y): Region
    self.depth = depth # int
    self.target = target # (x, y)
    self.populate()

  def populate(self):
    for y in range(0, self.target[0] + 5):
      for x in range(0, self.target[1] + 5):
        self.regions[(x, y)] = Region(x, y, self.depth)
        if x > 0:
          self.regions[(x, y)].xminus1 = self.regions[(x - 1, y)]
        if y > 0:
          self.regions[(x, y)].yminus1 = self.regions[(x, y - 1)]
    # TODO: fix this private access
    self.regions[(0, 0)]._geologic_index = 0
    self.regions[target]._geologic_index = 0
    #for y in range(0, self.target[0] + 5):
    #  for x in range(0, self.target[1] + 5):

  def draw(self):
    s = ""
    for y in range(0, self.target[0] + 5):
      for x in range(0, self.target[1] + 5):
        symbol = self.regions[(x, y)].region_type()
        if (x, y) == target:
          s += "T"
        else:
          s += symbol
      s += "\n"
    print s

# main
#depth = 6084
#target = (14, 709)
depth = 510
target = (10, 10)
cave = Cave(depth, target)
cave.draw()
