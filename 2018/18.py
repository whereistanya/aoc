#!/usr/bin/env python
# Advent of code Day 18.

class Coord(object):
  """Coordinates from our list."""
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.landscape = None
    self.next_landscape = None

  def __repr__(self):
    return "Coord: %d,%d, landscape: %s" % (self.x, self.y, self.landscape)

  def moves(self):
    x = self.x
    y = self.y
    north = (x, y - 1)
    northeast = (x + 1, y - 1)
    east = (x + 1, y)
    southeast = (x + 1, y + 1)
    south = (x, y + 1)
    southwest = (x - 1, y + 1)
    west = (x - 1, y)
    northwest = (x - 1, y - 1)
    directions = [north, northeast, east, southeast,
                  south, southwest, west, northwest]
    return directions

class Ground(object):
  def __init__(self, lines):
    self.coords = {}
    self.max_x = 0
    self.max_y = len(lines)
    self.populate(lines)

  def populate(self, lines):
    for y in range(0, len(lines)):
      line = lines[y].strip()
      if len(line) > self.max_x:
        self.max_x = len(line)
      for x in range(0, len(line.strip())):
        letter = line[x]
        coord = Coord(x, y)
        self.coords[(x, y)] = coord
        if letter == "#":
          coord.landscape = "#"
        elif letter == "|":
          coord.landscape = "|"
        elif letter == ".":
          coord.landscape = "."
        else:
          print("Bad input", letter)
          sys.exit(1)

  def value(self):
    woods = 0
    lumberyards = 0
    for coord in list(self.coords.values()):
      if coord.landscape == "#":
        lumberyards += 1
      elif coord.landscape == "|":
        woods += 1
    return lumberyards * woods

  def draw(self):
    for y in range (0, self.max_y):
      s = ""
      for x in range (0, self.max_x):
        coord = self.coords[(x, y)]
        s += coord.landscape
      print(s)
    print()

  def mutate(self):
    # First figure out what the next states should be.
    for coord in list(self.coords.values()):
      counts = {}
      for x, y in coord.moves():
        if x < 0 or y < 0:
          continue
        if x >= self.max_x or y >= self.max_y:
          continue
        adjacent_coord = self.coords[(x, y)]
        try:
          counts[adjacent_coord.landscape] += 1
        except KeyError:
          counts[adjacent_coord.landscape] = 1
      if coord.landscape == ".":
        if "|" in counts and counts["|"] >= 3:
          coord.next_landscape = "|"
        else:
          coord.next_landscape = "."
      if coord.landscape == "|":
        if "#" in counts and counts["#"] >= 3:
          coord.next_landscape = "#"
        else:
          coord.next_landscape = "|"
      if coord.landscape == "#":
        if "|" in counts and "#" in counts and counts["#"] >= 1 and counts["|"] >= 1:
          coord.next_landscape = "#"
        else:
          coord.next_landscape = "."
    # Then make all the changes at once.
    for coord in list(self.coords.values()):
      coord.landscape = coord.next_landscape
    return self.coords


with open("day18input.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
  ".#.#...|#.",
  ".....#|##|",
  ".|..|...#.",
  "..|#.....#",
  "#.#|||#|#|",
  "...#.||...",
  ".|....|...",
  "||...#|.#|",
  "|.||||..|.",
  "...#.|..|.",
]
#"""

ground = Ground(lines)
#ground.draw()

n1 = 10           # part1
n2 = 1000000000   # part2

# From 429 onwards, the pattern loops every 28
i = 0
while True:
  i += 1
  coords = ground.mutate()
  value = ground.value()

  if i in [n1, n2]:
    print("Resource value for %d is %d" % (i, value))

  if i <= 428: # it takes 400 mutations for the pattern to settle
    continue
  while i + 28 < n2:
    i += 28
