#!/usr/bin/env python
# advent of code day 20

import math
import re

class Edge(object):
  def __init__(self, string):
    self.string = string
    self.side1 = None  # Tile
    self.side2 = None  # Tile

  def other_side(self, tile_number):
    if tile_number == self.side1.number:
      return side2
    else:
      return side1

class Tile(object):
  def __init__(self, number):
    self.number = number
    self.lines = []
    self.edges = []  # [str, str, ...] Order: N, E, S, W

  def N(self): return self.edges[0]
  def E(self): return self.edges[1]
  def S(self): return self.edges[2]
  def W(self): return self.edges[3]

  def generate_edges(self):
    edges = []
    edges.append(self.lines[0])
    edges.append("".join([column[-1] for column in self.lines]))
    edges.append(self.lines[-1])
    edges.append("".join([column[0] for column in self.lines]))
    self.edges = edges

  def match_edge(self, edge):
    if edge in self.edges or edge[::-1] in self.edges:
      return True
    return False

  def match_edge_at_orientation(self, edge, needed):
    if needed == "W": fn = self.W
    if needed == "N": fn = self.N
    if not self.match_edge(edge):
      return None

    i = 0
    while i < 4:
      if(fn() == edge):
        return True
      self.rotate()
      i += 1

    self.flip()
    i = 0
    while i < 4:
      if(fn() == edge):
        return True
      self.rotate()

  def rotate(self):
    #print "Rotating", pattern
    newrows = []
    for i in range(len(self.lines)):
      # turn columns into rows by creating new lists with the 1st element of
      # each row, then the 2nd, etc. [::-1] means we're starting with the last
      # row.
      newrows.append("".join([row[i] for row in self.lines[::-1]]))
    self.lines = newrows
    self.generate_edges()

  def flip(self):
    self.lines.reverse()

  def strip_margins(self):
    newlines = []
    for line in self.lines[1:-1]:
      newlines.append(line[1:-1])
    self.lines = newlines

class Grid(object):
  def __init__(self):
    self.positions = {} # ((x,y): Tile)
    self.edges = {}  # str: Edge
    self.width = 0
    self.tile_height = 0
    self.tiles = []
    self.big_grid = []
    self.roughness = 0

  def add(self, position, tile):
    self.positions[position] = tile

  def parse(self, lines):
    tile = None
    tiles = []
    for line in lines:
      if line.startswith("Tile"):
        number = line.split(" ")[1].split(":")[0]
        tile = Tile(number)
        tiles.append(tile)
      elif line == "":
        continue
      else:
        tile.lines.append(line)
    self.tiles = tiles
    self.width = int(math.sqrt(len(self.tiles)))
    self.tile_height = len(self.tiles[0].lines) # arbitrary first tile

  def generate(self):
    for tile in self.tiles:
      tile.generate_edges()

  def match_edge(self, edge_string, first_tile):
    """Return the tile that matches, already flipped/rotated."""
    for tile in self.tiles:
      if tile == first_tile:
        continue
      # Already flipped and rotated
      if tile.match_edge(edge_string):
        return tile

  def print_grid(self):
    for y in range(0, 11):
      s = ""
      for x in range(0, 11):
        if (x, y) in self.positions:
          value = self.positions[(x, y)].number
        else:
          value = "????"
        s += " %s " % value
      print(s)

  def find_tile_at(self, position):
    try:
      return self.positions[position]
    except KeyError:
      return None

  def find_tile_for(self, position):
    # if there is a tile north of here, find its south edge,
    # match it against all tiles, rotate our found tile until its matching edge
    # points north.
    N = self.find_tile_at((position[0], position[1] - 1))
    if N:
      edge_to_find = N.S()
      edge_orientation_needed = "N"
      tile_to_avoid = N
    else:
      W = self.find_tile_at((position[0] - 1, position[1]))
      if not W:
        print("BUG: expected a tile N or W of %d, %d" %
          (position[0], position[1]))
        exit()
      edge_to_find = W.E()
      edge_orientation_needed = "W"
      tile_to_avoid = W
    for tile in self.tiles:
      if tile == tile_to_avoid:
        continue
      if tile.match_edge_at_orientation(edge_to_find, edge_orientation_needed):
        return tile
    return None

  def populate(self, cornerZero):
    """Take the tile that's the NW corner and go from there."""
    while (True):
      # rotate it until N and W have no matching edges
      N = self.match_edge(cornerZero.N(), cornerZero)
      E = self.match_edge(cornerZero.E(), cornerZero)
      S = self.match_edge(cornerZero.S(), cornerZero)
      W = self.match_edge(cornerZero.W(), cornerZero)
      if N is None and W is None:
        break
      cornerZero.rotate()
    self.add((0, 0), cornerZero)

    for y in range(0, self.width):
      for x in range(0, self.width):
        if (x, y) in self.positions:
          # We already found it. Move on.
          continue
        tile = self.find_tile_for((x, y))
        self.add((x, y), tile)

  def strip_margins(self):
    for tile in self.tiles:
      tile.strip_margins()
    self.tile_height -= 2


  def join(self):
    tile_y = 0
    while tile_y < self.width:
      this_row = [self.find_tile_at((x, tile_y)) for x in range(0, self.width) ]
      for y in range(0, self.tile_height):
        s = ""
        for tile in this_row:
          s += tile.lines[y]
        self.big_grid.append(s)
      tile_y += 1

  def find_corners(self):
    corners = []
    for tile in grid.tiles:
      edge_count = 0
      for edge in tile.edges:
        matched_edge = grid.match_edge(edge, tile)
        if matched_edge:
          edge_count += 1
      if (edge_count == 2):
        corners.append(tile)
    return corners

  def rotate(self):
    newrows = []
    for i in range(len(self.big_grid)):
      # turn columns into rows by creating new lists with the 1st element of
      # each row, then the 2nd, etc. [::-1] means we're starting with the last
      # row.
      newrows.append("".join([row[i] for row in self.big_grid[::-1]]))
    self.big_grid = newrows
 
  def flip(self):
    self.big_grid.reverse()

  def find_monsters(self):
    """
    ....................#
    #....##....##....###.
    .#..#..#..#..#..#....
    """
    head_re = "..................#."
    body_re = "#....##....##....###"
    feet_re = ".#..#..#..#..#..#..."
    count = 0
    monster_count = 0
    inside_monster_count = 0
    height = len(self.big_grid)
    for i in range(0, (height - 1)):
      if i == 0:
        continue
      if i == (height - 1):
        continue
      row = self.big_grid[i]
      matches = re.finditer(body_re, row)
      if not matches:
        continue
      for match in matches:
        start = match.start() # - 1 # dunno why
        end = match.end()

        prev = self.big_grid[i - 1]
        body_string = row[start:end]
        found_head = re.search(head_re, prev[start:end])
        if found_head is None:
          continue
        head_string = prev[start:end]
        following = self.big_grid[i + 1]
        found_feet = re.search(feet_re, following[start:end])
        if found_feet is None:
          continue
        feet_string = following[start:end]
        #print("Found a sea monster on line %d!" % i)
        monster_count += 1

    if monster_count == 0:
      return False
    for row in self.big_grid:
      for letter in row:
        if letter == '#':
          count += 1
    self.roughness = (count - (monster_count * 15)) # 15 #s per monster
    return True

inputfile = "input20.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

grid = Grid()
grid.parse(lines)
grid.generate()

# Part 1
corners = grid.find_corners()
product = 1
for corner in corners:
  product *= int(corner.number)

print("Part 1: product was %d" % product)

# Part 2.
grid.populate(cornerZero=corners[0])
grid.print_grid()
grid.strip_margins()
grid.join()

i = 0
found = False
while (i < 4):
  found = grid.find_monsters()
  if found:
    break
  grid.rotate()
  i += 1

if not found:
  grid.flip()
  i = 0

while (i < 4):
  found = grid.find_monsters()
  if found:
    break
  grid.rotate()
  i += 1

print("Part 2: Water roughness was %d" % (grid.roughness))
