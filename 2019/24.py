#!/usr/bin/python

import os
import time

class Eris(object):
  def __init__(self):
    self.squares = [False] * 25
    self.seen = set()  # biodiversities

  def alive(self, x):
    count = 0
    if x - 5 >= 0: # north
      count += self.squares[x - 5]
    if x + 5 < len(self.squares): # south
      count += self.squares[x + 5]
    if x % 5 != 4: # east
      count += self.squares[x + 1]
    if x % 5 != 0: # west:
      count += self.squares[x - 1]

    #print x, count
    if self.squares[x] and count == 1:
      return True
    if not self.squares[x] and count in [1, 2]:
      return True
    return False

  def display(self):
    os.system('clear')
    s = ""
    for i in range(len(self.squares)):
      if self.squares[i]:
        s += "#"
      else:
        s += "."
      if i % 5 == 4:
        s += "\n"
    print s

  def set(self, lines):
    i = 0
    for char in lines:
      if char == "\n":
        continue
      if char == "#":
        self.squares[i] = True
      else:
        self.squares[i] = False
      i += 1

  def run(self):
    for layout in range(0, 25000):
      state = []
      biodiversity = 0
      n = 1
      for i in range(len(self.squares)):
        if self.alive(i):
          state.append(True)
          biodiversity += n
        else:
          state.append(False)
        n *= 2
      self.squares = state
      #print tile, biodiversity
      if biodiversity in self.seen:
        print layout, biodiversity
        break
      self.seen.add(biodiversity)
      # Uncomment to visualise.
      # self.display()
      # time.sleep(0.5)

# Test
lines = """....#
#..#.
#..##
..#..
#...."""

# Live
lines = """..##.
..#..
##...
#....
...##"""

eris = Eris()
eris.set(lines)
eris.display()
eris.run()
