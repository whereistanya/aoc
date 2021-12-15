#!/usr/bin/env python
import os

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test():
  return [x.strip() for x in """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split("\n")]

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Point(object):
  def __init__(self, x, y, energy, grid):
    self.x = x
    self.y = y
    self.energy = int(energy)
    self.color = color.YELLOW
    self.grid = grid

  def neighbours(self):
    return self.grid.neighbours((self.x, self.y))

class Grid(object):
  def __init__(self, lines):
    self.lines = lines # [str, str, ...]
    self.grid = {}  # (x, y): int
    self.populate()
    self.height = len(lines)
    self.width = len(lines[0])

  def neighbours(self, point, diagonal=True):
    x, y = point
    neighbours = []
    for neighbour in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
      if neighbour in self.grid:
        neighbours.append(self.grid[neighbour])
    if diagonal:
      for neighbour in [(x + 1, y + 1), (x + 1, y - 1),
                        (x - 1, y + 1), (x - 1, y - 1)]:
        if neighbour in self.grid:
          neighbours.append(self.grid[neighbour])
    return neighbours

  def populate(self):
    for y in range(0, len(self.lines)):
      for x in range(0, len(self.lines[y])):
        self.grid[(x, y)] = Point(x, y, self.lines[y][x], self)

  def printgrid(self):
    for y in range(self.height):
      s = ""
      for x in range(self.width):
        s += (self.grid[(x, y)].color + "%d" % self.grid[(x, y)].energy +
              color.END)
      print(s)
    print("\n")

lines = test()
grid = Grid(lines)

# Part 1

path = []
start = grid.grid[(0, 0)]
start.color = color.GREEN
end = grid.grid[(grid.width - 1, grid.height - 1)]
end.color = color.RED
grid.printgrid()

def findpath():
  pass
