#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test():
  return [x.strip() for x in """2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n")]

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
  def __init__(self, x, y, height, grid):
    self.x = x
    self.y = y
    self.height = int(height)
    self.color = color.YELLOW
    self.grid = grid

  def neighbours(self):
    return self.grid.neighbours((self.x, self.y))

class Grid(object):
  def __init__(self, lines):
    self.lines = lines # [str, str, ...]
    self.grid = {}  # (x, y): int
    self.populate()

  def neighbours(self, point):
    x, y = point
    neighbours = []
    for neighbour in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
      if neighbour in self.grid:
        neighbours.append(self.grid[neighbour])
    return neighbours

  def populate(self):
    for y in range(0, len(self.lines)):
      for x in range(0, len(self.lines[y])):
        self.grid[(x, y)] = Point(x, y, self.lines[y][x], self)

  def printgrid(self):
    for y in range(len(self.lines)):
      s = ""
      for x in range(len(self.lines[y])):
        s += (self.grid[(x, y)].color + "%d" % self.grid[(x, y)].height +
              color.END)
      print(s)

#lines = test()
print lines
grid = Grid(lines)

# Part 1
risk = 0
for point in grid.grid.values():
  lowest = True
  height = point.height
  for n in point.neighbours():
    if n.height <= height:
      lowest = False
      break
  if lowest:
    point.color = color.RED
    risk += (1 + height)
  else:
    point.color = color.BOLD

grid.printgrid()
print(risk)

# Part 2
to_visit = set()  # [Point, ...]
for k, point in grid.grid.iteritems():
  if point.height == 9:
    point.color = color.BOLD + color.YELLOW
  else:
    point.color = color.GREEN
    to_visit.add(point)

basins = []

colors = [color.CYAN, color.GREEN, color.PURPLE, color.RED, color.BLUE]
c = 0
while to_visit:
  start = to_visit.pop()
  basin_color = color.BOLD + colors[c % 5]
  c += 1
  start.color = basin_color
  current_basin = start.neighbours()
  basin_size = 1
  while current_basin:
    point = current_basin.pop()
    if point in to_visit:
      basin_size += 1
      to_visit.remove(point)
      point.color = basin_color
      current_basin.extend(point.neighbours())
  basins.append(basin_size)

grid.printgrid()
sorted_basins = sorted(basins, reverse=True)
print (sorted_basins[0] * sorted_basins[1] * sorted_basins[2])

