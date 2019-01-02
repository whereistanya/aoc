#!/usr/bin/env python
# Advent of code Day 23.

import re
import sys

import numpy as np
import pyoctree

class Nanobot(object):
  def __init__(self, x, y, z, r):
    self.x = x
    self.max_x = x + r
    self.min_x = x - r
    self.y = y
    self.max_y = y + r
    self.min_y = y - r
    self.z = z
    self.max_z = z + r
    self.min_z = z - r
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

  def overlaps(self, other):
    """How far away are the bots' ranges."""
    # if it's less than zero, their ranges overlap
    # but maxx/y/z doesn't work
    # if they have an x, a y and a z in common, does that work?
    if self.min_x > other.max_x or self.max_x < other.min_x:
      return False
    if self.min_y > other.max_y or self.max_y < other.min_y:
      return False
    if self.min_z > other.max_z or self.max_z < other.min_z:
      return False

    # this is not true probably?
    return True


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

"""
lines = [
"pos=<10,12,12>, r=2",
  "pos=<12,14,12>, r=2",
  "pos=<16,12,12>, r=4",
  "pos=<14,14,14>, r=6",
  "pos=<50,50,50>, r=200",
  "pos=<10,10,10>, r=5",
]
#"""

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

print "Part one: Strongest bot is", strongest_bot

in_range = 0
for bot in bots:
  if strongest_bot.in_range(bot):
    in_range += 1

print "%d bots in range" % in_range

"""
min_x = 1000000000
max_x = 0
min_y = 1000000000
max_y = 0
min_z = 1000000000
max_z = 0

for bot in bots:
  if bot.max_x > max_x:
    max_x = bot.max_x
  if bot.max_y > max_y:
    max_y = bot.max_y
  if bot.max_z > max_z:
    max_z = bot.max_z
  if bot.min_x < min_x:
    min_x = bot.min_x
  if bot.min_y < min_y:
    min_y = bot.min_y
  if bot.min_z < min_z:
    min_z = bot.min_z

print min_x, max_x, min_y, max_y, min_z, max_z
# -184808155 350229460 -143101429 290189682 -158623074 212838874
# big numbers!
"""

# heuristically...

p = 0
"""
approx = {} # int: number of bots
for bot in bots:
  #print bot
  x = bot.min_x
  while x < bot.max_x:
    y = bot.min_y
    while y < bot.max_y:
      z = bot.min_z
      while z < bot.max_z:
        #print (x, y, z)
        for other in bots:
          if (bot.in_range(other)):
            try:
              approx[(x, y, z)] += 1
            except KeyError:
              approx[(x, y, z)] = 1
            try:
              xes[x] += 1
            except KeyError:
              xes[x] == 1
        z += 100000000
      y += 100000000
    x += 100000000
"""

print len(bots)
overlaps = {}
for bot in bots:
  overlaps[bot] = 0

for bot in bots:
  #print bot
  for other in bots:
    if bot.overlaps(other):
      overlaps[bot] += 1

min_x = 0
min_y = 0
min_z = 0

for o in overlaps:
  if overlaps[o] > 990:
    print o

#sorted_overlaps = sorted(overlaps.items(), key=lambda x: x[1], reverse = True)

#print sorted_overlaps

# 90129540,43291201,69471683


