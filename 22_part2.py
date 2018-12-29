#!/usr/bin/env python
# Advent of code Day 22

import sys

class Region(object):
  def __init__(self, x, y, depth):
    self.x = x
    self.y = y
    self.is_target = False
    self.depth = depth
    self._region_type = -1
    self._erosion_level = -1
    self._geologic_index = -1
    self.neighbours = {} # (x, y) : Region

  def __repr__(self):
    # TODO: return sumbol
    return "Region(%d,%d: (%d)" % (self.x, self.y, self._region_type)

  def moves(self):
    x, y = self.x, self.y
    moves = []
    for nearby_region in self.neighbours.values():
      for tool in nearby_region.possible_tools():
        moves.append((nearby_region, tool))
    return moves

  def possible_tools(self):
    if self._region_type == 0:   # rocky
      return ["climbing_gear", "torch"]
    elif self._region_type == 1:  # wet
      return ["climbing_gear", "neither"]
    elif self._region_type == 2:  # narrow
      return ["torch", "neither"]

  def region_type(self):
    if self._region_type >= 0:
      return self._region_type
    self.erosion_level()
    if self._region_type < 0:
      print "Still -1 after e_l()"
    return self._region_type

  def geologic_index(self):
    if self._geologic_index >= 0:
      return self._geologic_index
    if self.x == 0 and self.y == 0:
      self._geologic_index = 0
    elif self.is_target:
      self._geologic_index = 0
    elif self.y == 0:
      self._geologic_index = self.x * 16807
    elif self.x == 0:
      self._geologic_index = self.y * 48271
    else:
      self._geologic_index = self.xminus1.erosion_level() * self.yminus1.erosion_level()
    return self._geologic_index

  def erosion_level(self):
    if self._erosion_level >= 0 and self.region_type >= 0:
      return self._erosion_level
    self._erosion_level = (self.geologic_index() + self.depth) % 20183
    self._region_type = self._erosion_level % 3
    return self._erosion_level

class Cave(object):
  def __init__(self, depth, target):
    self.regions = {}  # ((x,y): Region
    self.depth = depth # int
    self.target = target # (x, y)
    self.populate()

  def populate(self):
    for y in range(0, self.target[1] + 7):
      for x in range(0, self.target[0] + 7):
        self.regions[(x, y)] = Region(x, y, self.depth)
        if x > 0:
          self.regions[(x, y)].xminus1 = self.regions[(x - 1, y)]
        if y > 0:
          self.regions[(x, y)].yminus1 = self.regions[(x, y - 1)]
    self.regions[target].is_target = True
    for y in range(0, self.target[1] + 7):
      for x in range(0, self.target[0] + 7):
        region = self.regions[(x, y)]
        north = (x, y - 1)
        south = (x, y + 1)
        west = (x - 1, y)
        east = (x + 1, y)
        for direction in [north, south, east, west]:
          if direction in self.regions:
            region.neighbours[direction] = self.regions[direction]


  def draw(self):
    symbols = {
      0: ".",  # rocky
      1: "=",  # wet
      2: "|",  # narrow
    }

    s = ""
    for y in range(0, self.target[1] + 6):
      for x in range(0, self.target[0] + 6):
        symbol = symbols[self.regions[(x, y)].region_type()]
        if (x, y) == target:
          s += "T"
        else:
          s += symbol
      s += "\n"
    print s

# main
depth = 510
target = (10, 10)
#depth = 6084
#target = (14, 709)
cave = Cave(depth, target)
cave.draw()

to_check = [(cave.regions[(0, 0)], "torch")]

while to_check:
  starting_point, tool = to_check.pop(0)
  print starting_point, tool
  print starting_point.moves()

  # DFS with memozation.


