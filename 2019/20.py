#!/usr/bin/python

import collections
import sys

class Grid(object):
  def __init__(self):
    self.squares = {}
    self.portalnames = {} # (x, y): str
    self.portals = {} # (x, y): (x, y)
    self.letters = set()
    self.height = 0
    self.width = 0
    self.start = None
    self.end = None
    self.checked = set()

  def neighbours(self, x, y):
    return [(x-1, y, x-2, y),
            (x, y-1, x, y-2),
            (x+1, y, x+2, y),
            (x, y+1, x, y+2)
           ]

  def get(self, x, y):
    try:
      return self.squares[(x, y)]
    except KeyError:
      return ""

  def populate(self, lines):
    self.height = len(lines)
    for y in range(self.height):
      line = lines[y].rstrip()
      width = len(line)
      if width > self.width:
        self.width = width
      for x in range(width):
        char = line[x]
        self.squares[(x, y)] = char
        if char.isupper():
          self.letters.add((x, y))

    # pair up these letters to find portals
    pairs = {}
    while len(self.letters) > 0:
      x, y = self.letters.pop()
      for (x1, y1, x2, y2) in self.neighbours(x, y):
        found = False
        if self.get(x1, y1).isupper():
          location = None
          if self.get(x2, y2) == ".":
            if (x > 5 and x < (self.width - 5) and y > 5 and y < (self.height - 5)):
                  #self.squares[(x2, y2)] = "|"
                  location = -1 # inside
            else:
              #self.squares[(x2, y2)] = "*"
              location = 1 # outside
            name = "".join(sorted([self.get(x, y), self.get(x1, y1)]))
            self.portalnames[(x2, y2)] = name
            self.letters.remove((x1, y1))
            found = True
            if name == "AA":
              self.start = (x2, y2)
              break
            if name == "ZZ":
              self.end = (x2, y2)
              break
            if name in pairs:  # we found the other exit
              self.portals[(x2, y2)] = (pairs[name][0], pairs[name][1], location * -1)
              self.portals[pairs[name]] = (x2, y2, location)
            else:
              pairs[name] = (x2, y2)
            break
      if not found:
        self.letters.add((x,y))

    # Sanity check. AA and ZZ shouldn't have pairs.
    #entrances = []
    #for s in self.squares:
    #  if self.squares[s] == "*":
    #    entrances.append(s)
    #assert len(entrances) == len(self.portals) + 2
    #print sorted(self.portals.keys())
    #print "Found %d portals" % (len(self.portals))
    #print "Found %d entrances" % len(entrances)
    #print sorted(entrances)


  def display(self, level):
    s = ""
    for y in range(0, self.height):
      for x in range(0, self.width):
        if x == self.start[0] and y == self.start[1] and level == 1:
          s += "@"
          continue
        if x == self.end[0] and y == self.end[1] and level == 1:
          s += "$"
          continue
        if (x, y, level) in self.checked:
          s += ","
        else:
          try:
            s += self.squares[(x, y)]
          except KeyError:
            s += " "
      s += "\n"
    print(s)

  def bfs(self, start):
    # starting level is zero. Level inside it is one. Zero is outside layer.
    to_check = collections.deque()
    x, y = start
    level = 1
    to_check.append((x, y, level))
    steps = 0
    while to_check:
      this_step = list(to_check)
      to_check.clear()
      for i in range(len(this_step)):
        x, y, level = this_step[i]
        self.checked.add((x, y, level))
        if x == self.end[0] and y == self.end[1] and level == 1:
          print("Found the end in %d steps" % steps)
          sys.exit(0)
        for neighbour in self.neighbours(x, y):
          x1, y1, _, _ = neighbour
          if self.get(x1, y1) == "." and (x1, y1, level) not in self.checked:
            if (x1, y1, level) not in to_check:
              to_check.append((x1, y1, level))
        if (x, y) in self.portals:
          x1, y1, levelchange = self.portals[(x, y)]
          level1 = level + levelchange
          if level1 <= 0:
            continue
          if (x1, y1, level1) in self.checked:
            continue
          if (x1, y1, level1) in to_check:
            continue
          to_check.append((x1, y1, level1))
      steps += 1

with open("input20.txt") as f:
  lines = f.readlines()

grid = Grid()
grid.populate(lines)
grid.display(1)
print(grid.start)
print(grid.end)
grid.bfs(grid.start)
