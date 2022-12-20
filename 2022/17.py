#!/usr/bin/env python3

import math

filename = "input17.txt"
filename = "test17.txt"


class Game(object):
  def __init__(self, jets):
    self.width = 7
    self.height = 30
    self.grid = set() # fallen rocks not current rock
    self.current = []
    self.next_rock = 0
    self.jets = jets
    self.next_jet = 0
    self.adjust_x = 0
    self.adjust_y = 0

  def print(self):
    print (self.grid)
    for y in range(self.height):
      s = ""
      for x in range(self.width):
        if (x, y) in self.grid:
          s += "#"
        elif (x, y) in self.current:
          s += "@"
        else:
          s += "."
      print(s)

  def get_rock(self, i):
    rocks = [
      [(0, 0), (1, 0), (2, 0), (3, 0)], # horizontal
      [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], # cross
      [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)], # ell
      [(0, 0), (0, 1), (0, 2), (0, 3)], # vertical
      [(0, 0), (1, 0), (0, 1), (1, 1)], # square
    ]
    return rocks[i]

  def move_jets(self):
    c = self.jets[self.next_jet % len(self.jets)]
    if c == "<":
      self.adjust_x -= 1
    elif c == ">":
      self.adjust_x += 1
    else:
      print("BUG: unexpected input:", c)
      exit(1)
    self.adjust_current()
    self.next_jet += 1

  def drop_rock(self):
    # new rock, set standard position
    self.adjustment = (3, 0) # rock is +3x, unchanged y
    self.current = self.get_rock(self.next_rock)
    self.adjust_current()
    self.print()
    self.move_jets()
    self.print()
    self.adjust_y += 1
    self.adjust_current()
    self.print()



  def adjust_current(self):
    adjx = self.adjust_x
    adjy = self.adjust_y
    self.current = [(x + adjx, y + adjy) for (x, y) in self.current]


with open(filename, "r") as f:
  data = f.read().strip()

entry = 2 # two units away from the left wall
          # bottom edge is three units above the highest rock in the room


game = Game(data)
game.print()
game.drop_rock()
game.print()
