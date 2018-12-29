#!/usr/bin/env python
# Advent of code Day 23.

import re
import sys

class Nanobot(object):
  def __init__(self, x, y, z, r):
    self.x = x
    self.y = y
    self.z = z
    self.r = r
    self.others = {}  # {Nanobot: distance}

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.z == other.z

  def __repr__(self):
    return "Nanobot(%d,%d,%d : %d)" % (self.x, self.y, self.z, self.r)

  def in_range(self, other):
    """Range to the bot itself is zero and is not excepted."""
    if other in self.others:
      return self.others[other] <= self.r
    distance = abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
    self.others[other] = distance
    other.others[self] = distance

    return distance <= self.r


with open("day23input.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
  "pos=<0,0,0>, r=4",
  "pos=<1,0,0>, r=1",
  "pos=<4,0,0>, r=3",
  "pos=<0,2,0>, r=1",
  "pos=<0,5,0>, r=3",
  "pos=<0,0,3>, r=1",
  "pos=<1,1,1>, r=1",
  "pos=<1,1,2>, r=1",
  "pos=<1,3,1>, r=1",
]
"""

bots = []

line_re = "^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)"

strongest = 0
strongest_bot = None

for line in lines:
  try:
    groups = re.search(line_re, line.strip()).groups()
    x, y, z, r = [int(x) for x in groups]
  except AttributeError:
    print "Couldn't match", line

  bot = Nanobot(x, y, z, r)
  if bot.r > strongest:
    strongest = r
    strongest_bot = bot
  bots.append(bot)

print "Strongest bot is", strongest_bot

in_range = 0
for bot in bots:
  if strongest_bot.in_range(bot):
    in_range += 1

print "%d bots in range" % in_range
