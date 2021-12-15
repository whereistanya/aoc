#!/usr/bin/env python

import os
import time

def real():
  return [x.strip() for x in """6227618536
2368158384
5385414113
4556757523
6746486724
4881323884
4648263744
4871332872
4724128228
4316512167""".split("\n")]

def test():
  return [x.strip() for x in """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n")]

def test2():
  return [x.strip() for x in """11111
19991
19191
19991
11111""".split("\n")]

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
    for y in range(len(self.lines)):
      s = ""
      for x in range(len(self.lines[y])):
        s += (self.grid[(x, y)].color + "%d" % self.grid[(x, y)].energy +
              color.END)
      print(s)
    print("\n")

lines = real()
grid = Grid(lines)

# Part 1
grid.printgrid()

def step():
  flashed = set()
  flash_count = 0
  # First, the energy level of each octopus increases by 1
  for k, point in grid.grid.iteritems():
    point.color = color.YELLOW
    point.energy += 1

  # Then, any octopus with an energy level greater than 9 flashes
  # This increases the energy level of all adjacent octopuses by 1
  while True:
    something_new_flashed = False
    for k, point in grid.grid.iteritems():
      if point.energy > 9 and point not in flashed:
        something_new_flashed = True
        flash_count += 1
        point.color = color.RED
        flashed.add(point)
        for neighbour in point.neighbours():
          neighbour.energy += 1
    if not something_new_flashed:
      for point in flashed:
        point.energy = 0
      break
  return flash_count

octocount = len(grid.grid)
count = 0
i = 0
after100 = 0
while True:
  time.sleep(0.01)
  os.system("clear")
  grid.printgrid()
  print(i, count)
  flashcount = step()
  count += flashcount
  i += 1
  if i == 100:
    after100 = count
  if flashcount == octocount:
    break

print("Part1: After 100 flashes: %d" % count)
print("Part2: All flashed after %d steps" % i)
