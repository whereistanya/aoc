#!/usr/bin/env python

test = False
#test = True

DEBUG = False

import sys
sys.path.append("../../")
import util.grid as gridlib
import math

filename = "input.txt"
if test:
  filename = "test1"

class Robot(object):
  def __init__(self, name, grid, controlled): # controlled: what this thing controls
    self.name = name
    self.grid = grid
    self.pos = grid.get_by_char("A")[0]
    self.controlled = controlled
    self.controller = None
    self.typed = ""
    self.bestcode = {}  # (a, b): str   -- best code from a to b. If not populated, calculate it.
    self.pathcache = {}


  def move(self, instruction):
    if DEBUG: print(self.name, "Instruction:", instruction)
    fns = {
      "<": self.left,
      "^": self.up,
      ">": self.right,
      "v": self.down,
      "A": self.activate,
    }
    fn = fns[instruction]
    fn()

  def up(self):
    self.pos = self.grid.n(self.pos)
    if DEBUG: print(self.name, "Moved to pos:", self.pos)

  def down(self):
    self.pos = self.grid.s(self.pos)
    if DEBUG: print(self.name, "Moved to pos:", self.pos)

  def right(self):
    self.pos = self.grid.e(self.pos)
    if DEBUG: print(self.name, "Moved to pos:", self.pos)

  def left(self):
    self.pos = self.grid.w(self.pos)
    if DEBUG: print(self.name, "Moved to pos:", self.pos)

  def activate(self):
    if DEBUG: print(self.name, "Activating at position", self.pos)
    fns = {
      "<": self.controlled.left,
      "^": self.controlled.up,
      ">": self.controlled.right,
      "v": self.controlled.down,
      "A": self.controlled.activate,
    }
    fn = fns[self.pos.value]
    self.typed += self.pos.value
    fn()

  def print(self):
    print("Robot: %s at Pos: %s" % (self.name, self.pos))
    self.grid.printnocolor()
    print()


  def find_best_code_from_to(self, start, chars):
    """ start is a char, chars is multuple. Handle one at a time. Recurses and caches at each step"""
    if DEBUG: print(self.name, "looking for best code from", start, "to", chars)
    #if (start, chars) in self.bestcode:
    #  return self.bestcode[(start, chars)]

    length = 0

    pos = start
    for c in chars:
      if DEBUG: print(self.name, "Looking for a path for char", c)
      if (pos, c) in self.bestcode:
        length += self.bestcode[(pos, c)]
        if DEBUG: print(self.name, "That code is cached! Best code for", pos, "to", c, "is", self.bestcode[(pos, c)])
        pos = c
        continue
    # generate the best code for this char only
      if (pos, c) in self.pathcache:
        possible_paths = self.pathcache[(pos,c)]
      else:
        possible_paths = self.find_all_paths(pos, c)
        self.pathcache[(pos,c)] = possible_paths
      shortest = math.inf # shortest path to get this char from here
      if DEBUG: print(self.name, len(possible_paths), "paths found from", pos, "to", c)
      for path in possible_paths: # make it downstream's problem!
        path = path + "A" # need to click A when we get there
        # go downstream to get the best code for this path
        if DEBUG: print(self.name, "Trying this path:", path)
        if self.controller is None:
          print(self.name, "has no controller")
          exit()
        codelen = self.controller.find_best_code_from_to("A", path)
        if DEBUG: print(self.name, "Downstream says the best code for", path, "is:", codelen)
        if codelen < shortest:
          #shortcode = code
          shortest = codelen

      # we now have the shortest code for this character
      #bestcode += shortcode
      length += shortest
      if DEBUG: print(self.name, "Caching fastest path from", pos, "to", c, "is", shortest)
      self.bestcode[(pos, c)] = shortest
      # next char will be from here
      pos = c
    #self.bestcode[(start, chars)] = length
    if DEBUG: print(self.name, "returning the best code for", chars, "is", length)
    return length


  def find_all_paths(self, start, end):
    # figure out all the direct paths from start to end (both are chars)
    # request each path from upstream with an X symbol in between as delineation
    # robots and humans need to recognize special char X as a newline I guess
    spos = self.grid.get_by_char(start)[0]
    epos = self.grid.get_by_char(end)[0]

    def translate(d):
      if d == "north":
        return "^"
      if d == "south":
        return "v"
      if d == "east":
        return ">"
      if d == "west":
        return "<"

    def dfs(p, end, grid, this_path, this_code, all_codes):
      if p == epos:
        all_codes.append(this_code)
        return
      neighbours = grid.neighbours_by_direction(p, diagonal=False)

      for d, n in neighbours.items():
        if n is None:
          continue
        if n.value == ".":
          continue
        if n in this_path:
          continue
        next_path = list(this_path)
        next_path.append(n)
        next_code = this_code + translate(d)
        dfs(n, epos, grid, next_path, next_code, all_codes)

    all_codes = []
    dfs(spos, epos, self.grid, [spos], "", all_codes)

    return all_codes




# A KeyPad is a robot with an overridden activate function
class KeyPad(Robot):
  def activate(self):
    #print(self.name, "ACTIVATING:", self.pos.value)
    self.typed += self.pos.value


# A Human is a robot that's responsible for its own choices and just writes things down. Profound.
class Human(Robot):
  def __init__(self, name):
    self.requested = ""
    self.name = name
    self.bestcode = {}

  def find_best_code_from_to(self, start, chars):
    if DEBUG: print(self.name, "looking for best code from", start, "to", chars)
    if DEBUG: print(self.name, "returning the chars it got", chars)
    return len(chars)

with open(filename, "r") as f:
  codes = [x.strip() for x in f.readlines()]



def setup(robotcount):
# grids just used for tracking own location
  numbergrid = gridlib.Grid(["789", "456", "123", ".0A"])
  directiongrid = gridlib.Grid([".^A", "<v>"])

  robots = [KeyPad("keypad", numbergrid, None) ] # only controls itself
  for i in range(1, robotcount + 1):
    robots.append(Robot("  robot%d" % i, directiongrid, robots[i - 1]))
  human = Human("      human") # controls robot2
  robots.append(human)

  for i in range(robotcount):
    robots[i].controller = robots[i + 1]
  robots[robotcount].controller = human

  return robots



part1 = 0
part2 = 0
debug = False

# Part 1
robotcount = 2
robots = setup(robotcount)

for code in codes:
  final_shortcode = robots[0].find_best_code_from_to("A", code)
  print(code, ":The shortest code is:", final_shortcode)
  part1 += final_shortcode * int(code[0:3])

# Part 2
robotcount = 25
robots = setup(robotcount)

for code in codes:
  final_shortcode = robots[0].find_best_code_from_to("A", code)
  print(code, ":The shortest code is:", final_shortcode)
  part2 += final_shortcode * int(code[0:3])


print("Part 1:", part1)
print("Part 2:", part2)

