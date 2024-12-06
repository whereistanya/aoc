#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"
#filename = "test1"


with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


part1 = 0
part2 = 0


class Guard(object):
  def __init__(self, position, grid):
    self.position = position
    self.grid = grid
    self.direction = "n"
    self.positions = set() # tuple of point, direction

  def move(self, markpath=False):
    if self.direction == "n":
      to = self.grid.n_xy(self.position)
    elif self.direction == "s":
      to = self.grid.s_xy(self.position)
    elif self.direction == "w":
      to = self.grid.w_xy(self.position)
    elif self.direction == "e":
      to = self.grid.e_xy(self.position)

    if to is None:
      self.grid.setvalue(self.position.x, self.position.y, ".")
      return "out"

    if self.grid.getpoint(to).value == "#":
      self.turn()
      self.move()
    else:
      if markpath:
        self.grid.setvalue(self.position.x, self.position.y, "X")
      else:
        self.grid.setvalue(self.position.x, self.position.y, ".")
      if (to, self.direction) in self.positions:
        return "loop"
      self.grid.setvalue(to.x, to.y, "^")
      self.position = to
      self.positions.add((to, self.direction))

  def turn(self):
    if self.direction == "n":
      self.direction = "e"
    elif self.direction == "s":
      self.direction = "w"
    elif self.direction == "w":
      self.direction = "n"
    elif self.direction == "e":
      self.direction = "s"

# start here

g = gridlib.Grid(lines)
guardpos = g.get_by_char("^")
print(guardpos)
if len(guardpos) > 1:
  print("Too many guards")
  exit()

guard = Guard(guardpos[0], g)

g.printgrid()
print("Guard at", guard.position)

# If there is something directly in front of you, turn right 90 degrees.
# Otherwise step forward


i = 0
while True:
  move = guard.move()
  i += 1
  if move == "out":
    break
print("out after", i, "moves")
  #print("Guard at", guard.position)
  #g.printgrid()

positions = g.get_by_char("X")
part1 = len(positions) + 1 # last one is the "out" space

print()
print()
print("Part 2")

# Part 2
g = gridlib.Grid(lines)
guardpos = g.get_by_char("^")
originalpos = guardpos[0]
guard = Guard(originalpos, g)

oneWest = g.w_xy(guardpos[0])
#g.setvalue(oneWest.x, oneWest.y, "#")
print(oneWest)
g.printgrid()

loopCount = 0
loopPoints = []

for point in g.grid.values():
  if point.value == "#":
    continue
  if point.value == "^":
    continue
  #g.printnocolor()
  g.setvalue(point.x, point.y, "#")
  guard.positions = set()
  guard.position = originalpos
  guard.direction = "n"

  i = 0
  while True:
    move = guard.move()
    i += 1
    if move == "out":
      #print("out after", i, "moves")
      break
    if move == "loop":
      loopCount += 1
      loopPoints.append(point)
      break
  g.setvalue(point.x, point.y, ".")

for p in loopPoints:
  g.setvalue(p.x, p.y, "O")

g.printgrid()

part2 = loopCount
print("Part 1:", part1)
print("Part 2:", part2)
