#!/usr/bin/env python
# Advent of code Day 22 part 2

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
    self.possible_tools = []
    self.xminus1 = None # neighbour
    self.yminus1 = None # neighbour

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
    """TODO: Quietly generates a lot of data. Should be more explicit."""
    if self._erosion_level >= 0 and self.region_type >= 0:
      return self._erosion_level
    self._erosion_level = (self.geologic_index() + self.depth) % 20183
    self._region_type = self._erosion_level % 3
    if self._region_type == 0:   # rocky
      self.possible_tools = ["climbing_gear", "torch"]
    elif self._region_type == 1:  # wet
      self.possible_tools = ["climbing_gear", "neither"]
    elif self._region_type == 2:  # narrow
      self.possible_tools = ["torch", "neither"]


    return self._erosion_level

class Move(object):
  def __init__(self, region, tool):
    self.region = region
    self.tool = tool
    self.neighbours = []  # [Move, ...]

  def __repr__(self):
    return "(%d,%d/%s)" % (
      self.region.x, self.region.y, self.tool[0])

class Cave(object):
  def __init__(self, depth, target, target_tool):
    self.regions = {}  # ((x,y): Region
    self.moves = {}  # ((x,y): [Move, ...]
    self.depth = depth # int
    self.target = target # (x, y)
    self.target_tool = "torch"
    self.max_x = self.target[0] + 100  # arbitrary!
    self.max_y = self.target[1] + 100
    self.target_move = None
    self.populate()
    assert self.target_move is not None

  def populate(self):
    # Generate the regions.
    for y in range(0, self.max_y):
      for x in range(0, self.max_x):
        self.regions[(x, y)] = Region(x, y, self.depth)
        if x > 0:
          self.regions[(x, y)].xminus1 = self.regions[(x - 1, y)]
        if y > 0:
          self.regions[(x, y)].yminus1 = self.regions[(x, y - 1)]
    self.regions[target].is_target = True

    # TODO(make this not load bearing haha wow)
    self.draw()

    # Now generate the moves.
    for region in self.regions.values():
      for tool in region.possible_tools:
        move = Move(region, tool)
        # TODO: gross
        if region.x == self.target[0] and region.y == self.target[1] and tool == self.target_tool:
          self.target_move = move
        try:
          self.moves[(region.x, region.y)].append(move)
        except KeyError:
          self.moves[(region.x, region.y)] = [move]

    # Now that all moves are created, wire up each move to its neighbours.
    # TODO: this layer of indirection is annoying.
    for movelist in self.moves.values():
      for move in movelist:
        x, y = move.region.x, move.region.y
        north = (x, y - 1)
        south = (x, y + 1)
        west = (x - 1, y)
        east = (x + 1, y)
        current = (x, y)
        for direction in [south, east, west, north, current]:
          if direction in self.moves:  # avoid stuff below 0 and above max
            neighbours = self.moves[direction]
            for neighbour in neighbours:
              if neighbour != move:
                move.neighbours.append(neighbour)

  def risk_level(self, min_x, min_y, max_x, max_y):
    risk = 0
    for y in range(min_y, max_y + 1):
      for x in range(min_x, max_x + 1):
        risk += self.regions[(x, y)].region_type()
    return risk

  def draw(self):
    symbols = {
      0: ".",  # rocky
      1: "=",  # wet
      2: "|",  # narrow
    }

    s = ""
    for y in range(0, self.max_y - 1):
      for x in range(0, self.max_x - 1):
        symbol = symbols[self.regions[(x, y)].region_type()]
        if (x, y) == target:
          s += "T"
        else:
          s += symbol
      s += "\n"
    #print s

  def shortest_path(self, source):
    print "Finding shortest path from", source
    print "I stole this dijkstra code from"
    print "https://gist.github.com/econchick/4666413"

    visited = {source: 0}
    path = {}

    nodes = []
    for v in self.moves.values():
      nodes.extend(v)
    nodes = set(nodes)

    while nodes:
      min_node = None
      for node in nodes:
        if node in visited:
          if min_node is None:
            min_node = node
          elif visited[node] < visited[min_node]:
            min_node = node
      if min_node is None:
        break

      nodes.remove(min_node)
      current_weight = visited[min_node]

      for edge in min_node.neighbours:
        if edge.tool == min_node.tool:
          move_weight = 1
        elif edge.region == min_node.region:
          move_weight = 7
        else:
          move_weight = 8
        weight = current_weight + move_weight
        if edge not in visited or weight < visited[edge]:
          visited[edge] = weight

    return visited[self.target_move]

# main

depth = 6084
target = (14, 709)
#depth = 510
#target = (10, 10)
#depth = 5
#target = (2,3)

#TODO: significance of depth?

# "once you reach the target, you need the torch equipped"
cave = Cave(depth, target, "torch")
cave.draw()
print "Part one: Risk level is", cave.risk_level(0, 0, target[0], target[1])
print

# We now have a graph of Moves each linked to their neighbours.
visited = set()
path = []

# TODO: messy. Data structures are wrong.
starting_region = cave.regions[0,0]
start_region_moves = cave.moves[(starting_region.x, starting_region.y)]
start = None
for move in start_region_moves:
  if move.tool == "torch":
    start = move
    break

assert start # not None

# I don't freakin know why -1
print "Part two: %d" % cave.shortest_path(start) - 1
