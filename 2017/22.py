#!/usr/bin/env python3

# Advent of code 2017 day 22

from enum import IntEnum

class Status(IntEnum):
  CLEAN = 0
  WEAKENED = 1
  INFECTED = 2
  FLAGGED = 3

class Direction(IntEnum):
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

class Grid(object):
  def __init__(self):
    self.infected = set()
    self.status = {}
    self.current = None
    self.direction = 0  # up. 1 is right, 2 is down, 3 is left
    self.infect_count = 0

  def draw(self):
    for y in range(-5, 6):
      s = ""
      for x in range(-5, 6):
        try:
          status = self.status[(x, y)]
        except KeyError:
          status = Status.CLEAN
        if (x, y) == self.current:
          s += "H"
        elif status == Status.CLEAN:
          s += "."
        elif status == Status.WEAKENED:
          s += "W"
        elif status == Status.INFECTED:
          s += "#"
        elif status == Status.FLAGGED:
          s += "F"
      print(s)
    print()

  def draw_part1(self):
    for y in range(-5, 6):
      s = ""
      for x in range(-5, 6):
        if (x, y) == self.current:
          s += "H"
        elif (x, y) in self.infected:
          s += "#"
        else:
          s += "."
      print(s)
    print()

  def populate(self, lines):
    for y in range(0, len(lines)):
      line = lines[y]
      for x in range(0, len(line)):
        if line[x] == "#":
          self.infected.add((x, y))
          self.status[(x, y)] = Status.INFECTED
    middle = (len(lines) - 1) / 2  # zero index makes this unintuitive
    self.current = (middle, middle)

  def move(self):
    # turn, change state of current node, move
    # Part 1
    #if self.current in self.infected:
    #  # turn left, clean the node, move
    #  self.direction = (self.direction + 1) % 4
    #  self.infected.remove(self.current)
    #else:
    #  # turn right, infect the node, move
    #  self.direction = (self.direction - 1) % 4
    #  self.infected.add(self.current)

    # Part 2
    try:
      status = self.status[self.current]
    except KeyError:
      status = Status.CLEAN # clean
    # Turn
    if status == Status.CLEAN:
      # turn left
      self.direction = Direction((self.direction - 1) % 4)
    elif status == Status.WEAKENED:
      # don't turn:
      pass
    elif status == Status.INFECTED:
      # turn right:
      self.direction = Direction((self.direction + 1) % 4)
    elif status == Status.FLAGGED:
      # reverse direction
      self.direction = Direction((self.direction + 2) % 4)
    else:
      print("unexpected status", status)
      exit()

    # change status
    self.status[self.current] = Status((status + 1) % 4)
    if self.status[self.current] == Status.INFECTED:
      self.infect_count += 1

    x, y = self.current
    if self.direction == Direction.UP:
      y -= 1
    elif self.direction == Direction.RIGHT:
      x += 1
    elif self.direction == Direction.DOWN:
      y += 1
    elif self.direction == Direction.LEFT:
      x -= 1
    else:
      print("direction shouldn't be", self.direction)
      exit()
    self.current = (x, y)

with open("input22.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
  "..#",
  "#..",
  "...",
]
#"""

grid = Grid()
grid.populate(lines)
grid.draw()

for i in range(0, 10000000):
  grid.move()


grid.draw()
print(grid.infect_count)
