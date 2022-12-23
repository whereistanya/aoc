#!/usr/bin/env python3

import math

filename = "test17.txt"
filename = "input17.txt"


class Game(object):
  def __init__(self, jets):
    self.width = 7
    self.height = 4
    self.grid = set() # fallen rocks not current rock
    self.current = []
    self.next_rock = 0
    self.jets = jets
    self.next_jet = 0
    self.floor = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    self.grid.update(self.floor)
    self.tower_height = 0

  def print(self):
    print("\n\n")

    for y in range(self.height, -1, -1):
      s = str(y).zfill(2)
      s += " "
      for x in range(-1, self.width + 1):
        if (x, y) in self.grid:
          s += "#"
        elif (x, y) in self.current:
          s += "@"
        elif (x, y) in self.floor:
          s += "-"
        elif x in [-1, 7]:
          s += "|"
        else:
          s += "."
      print(s)

  def can_move(self, pos):
    if any([p in self.grid for p in pos]):
      return False
    if any([x < 0 for (x, y) in pos]):
      return False
    if any([x > 6 for (x, y) in pos]):
      return False
    if any([y < 0 for (x, y) in pos]):
      return False
    return True

  def position_next_rock(self):
    rocks = [
      [(0, 0), (1, 0), (2, 0), (3, 0)], # horizontal
      [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], # cross
      [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], # ell
      [(0, 0), (0, 1), (0, 2), (0, 3)], # vertical
      [(0, 0), (1, 0), (0, 1), (1, 1)], # square
    ]
    rock = rocks[self.next_rock]
    adjx = 2
    adjy = self.height
    self.current = [(x + adjx, y + adjy) for (x, y) in rock]
    self.next_rock = (self.next_rock + 1) % 5

  def move_jets(self):
    c = self.jets[self.next_jet % len(self.jets)]
    if c == "<":
      #print("Push left")
      adjx = -1
    elif c == ">":
      #print("Push right")
      adjx = + 1
    else:
      print("BUG: unexpected input:", c)
      exit(1)
    self.next_jet += 1
    return adjx

  def drop_rock(self, i=0):
    self.position_next_rock()
    while True:
      adjx = self.move_jets()
      next_pos = [(x + adjx, y) for (x, y) in self.current]
      #if i == 763:
      #  print (next_pos)
      if self.can_move(next_pos):
        self.current = next_pos

      next_pos = [(x, y - 1) for (x, y) in self.current]
      if not self.can_move(next_pos):
        # stop moving
        self.grid.update(self.current)
        high_point = max([y for (x, y) in self.current])
        if high_point > self.tower_height:
          self.tower_height = high_point
        self.height = self.tower_height + 4
        break
      self.current = next_pos
      #self.print()


with open(filename, "r") as f:
  data = f.read().strip()

entry = 2 # two units away from the left wall
          # bottom edge is three units above the highest rock in the room


game = Game(data)
for i in range (2022):
  game.drop_rock()
  if ((i + 1) % 5 == 0):
    print(i + 1, game.tower_height)
print(i + 1, game.tower_height)
