#!/usr/bin/env python
# Advent of code Day 19

class Grid(object):
  def __init__(self, grid):
    self.grid = grid
    self.current = None
    self.direction = "down"
    self.get_start()
    self.letters = []
    self.moves = 0

  def move(self):
    x, y = self.current
  # move
    if self.direction == "down":
      y += 1
    elif self.direction == "up":
      y -= 1
    elif self.direction == "right":
      x += 1
    elif self.direction == "left":
      x -= 1
    self.current = (x, y)

    line = self.grid[(x, y)]
  # is there a letter here?
    if ord(line) in range(65, 92): # it's a letter
      print(line)
      self.letters.append(line)


  # set the direction for the next move
    if line == "+": # direction change
      # if we were going up or down, we're looking at the x value
      if self.direction in ["up", "down"]:
        if (x - 1, y) in list(self.grid.keys()) and self.grid[(x - 1, y)] != " ":
          self.direction = "left"
        else:
          self.direction = "right"
      # if we were going left or right, we're looking at the y value
      else:
        if (x, y - 1) in list(self.grid.keys()) and self.grid[(x, y - 1)] != " ":
          self.direction = "up"
        else:
          self.direction = "down"
    self.moves += 1

  def get_start(self):
    starting_point = None
    for x in range(0, width + 1):
      if (x, 0) in list(self.grid.keys()) and self.grid[(x, 0)] == "|":
        print("Found starting point")
        if starting_point is not None:
          print("Error: Found multiple starting points")
          exit()
        starting_point = (x, 0)
    if starting_point == None:
      print("didn't find a starting point")
    self.current = starting_point

  def display(self):
    for y in range (0, height + 1):
      s = ""
      for x in range (0, width + 1):
        if (x, y) == self.current:
          s += "#"
          continue
        try:
          s += self.grid[(x, y)]
        except KeyError:
          s += " "
      print(s)

with open("input19.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
"     |",
"     |  +--+",
"     A  |  C",
" F---|----E|--+",
"     |  |  |  D",
"     +B-+  +--+",
]
"""


diagram = {}
height = len(lines)
width = 0
# first line is y = 0
for y in range (0, height):
  line = lines[y]
  for x in range (0, len(line)):
    diagram[(x, y)] = line[x]
    if x > width:
      width = x

grid = Grid(diagram)
while True:
  try:
    grid.move()
  except KeyError:
    print("After", grid.moves, "moves, the letters were", "".join(grid.letters))
    break


