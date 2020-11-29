#!/usr/bin/python

import os
import sys
import time

class Eris(object):
  def __init__(self):

    self.squares = {} # level: [bool, bool, ...]
    self.squares[0] = [False] * 25
    self.seen = set()  # biodiversities

  def get(self, level, x):
    if (x == 12 and
        level in self.squares and
        x in self.squares[level] and
        self.squares[level][x]):
          print("Unexpected bug in level %d square 12" % (level))
          raise ValueError

    try:
      return self.squares[level][x]
    except KeyError:
      return False

  def alive(self, level, x):
    # The grid within level 0 is level 1
    # The grid outside level 0 is level -1
    if x == 12: # Middle square magic.
      return False

    count = 0
    ## Same level ##
    if x - 5 >= 0: # north
      count += self.get(level, x - 5)
    if x + 5 < 25: # south
      count += self.get(level, x + 5)
    if x % 5 != 4: # east
      count += self.get(level, x + 1)
    if x % 5 != 0: # west:
      count += self.get(level, x - 1)

    ## Look in the level surrounding this level (level - 1)
    if x in [0, 1, 2, 3, 4]:
      count += self.get(level - 1, 7)
    if x in [0, 5, 10, 15, 20]:
      count += self.get(level - 1, 11)
    if x in [4, 9, 14, 19, 24]:
      count += self.get(level - 1, 13)
    if x in [20, 21, 22, 23, 24]:
      count += self.get(level - 1, 17)

    ## Look in the center square of this level (level + 1)
    if x == 7: # above center tile
      for j in range(0, 5):
        count += self.get(level + 1, j)
    if x == 11: # west of center tile
      for j in [0, 5, 10, 15, 20]:
        count += self.get(level + 1, j)
    if x == 13: # east of center tile
      for j in [4, 9, 14, 19, 24]:
        count += self.get(level + 1, j)
    if x == 17: # above center tile
      for j in range(20, 25):
        count += self.get(level + 1, j)

    if self.get(level, x) and count == 1:
      return True
    if not self.get(level, x) and count in [1, 2]:
      return True
    return False

  def display(self, level = 0):
    s = ""
    print("=== LEVEL %d ===" % level)
    for i in range(25):
      if self.get(level, i):
        s += "#"
      elif i == 12:
        s += "?"
      else:
        s += "."
      if i % 5 == 4:
        s += "\n"
    #os.system('clear')
    print(s)

  def set(self, lines):
    # Initially, only level zero contains bugs.
    i = 0
    for char in lines:
      if char == "\n":
        continue
      if char == "#":
        self.squares[0][i] = True
      else:
        self.squares[0][i] = False
      i += 1
      assert self.squares[0][12] == False

  def run_part1(self):
    for layout in range(0, 25000):
      state = []
      biodiversity = 0
      n = 1
      for i in range(25):
        if self.alive(level, i):
          state.append(True)
          biodiversity += n
        else:
          state.append(False)
        n *= 2
      self.squares[0] = state
      #print tile, biodiversity
      if biodiversity in self.seen:
        print(layout, biodiversity)
        break
      self.seen.add(biodiversity)
      # Uncomment to visualise.
      #self.display(0)
      #time.sleep(0.5)


  def run_part2(self):
    states = {}
    minutes = 200
    print("######## LAYOUT 0 ########")
    self.display(0)
    for layout in range(1, minutes + 1):
      bugcount = 0
      level = 0
      for level in range (-120, 120):
        state = []
        for i in range(25):
          if self.alive(level, i):
            bugcount += 1
            state.append(True)
          else:
            state.append(False)
        states[level] = list(state)
      self.squares.clear()
      for state in states:
        self.squares[state] = states[state]

    print("######## LAYOUT %d ########" % layout)
    self.display(-5)
    self.display(-4)
    self.display(-3)
    self.display(-1)
    self.display(0)
    self.display(1)
    self.display(2)
    self.display(3)
    self.display(4)
    self.display(5)
    self.display(110) # Check we haven't underestimated how many levels we need
    print(bugcount)
    # Uncomment to visualise.
    #time.sleep(0.5)



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
eris.run_part2()
