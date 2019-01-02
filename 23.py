#!/usr/bin/env python
# Advent of code Day 23.

import re
import sys

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

# Part two

min_x = 1000000000000
max_x = 0
min_y = 1000000000000
max_y = 0
min_z = 1000000000000
max_z = 0

bot_count = 0
for bot in bots:
  bot_count += 1
  if bot.x > max_x:
    max_x = bot.x
  if bot.y > max_y:
    max_y = bot.y
  if bot.z > max_z:
    max_z = bot.z
  if bot.x < min_x:
    min_x = bot.x
  if bot.y < min_y:
    min_y = bot.y
  if bot.z < min_z:
    min_z = bot.z

print min_x, min_y, min_z
print max_x, max_y, max_z

# https://raw.githack.com/ypsu/experiments/master/aoc2018day23/vis.html
class Octree(object):
  def __init__(self):
    pass

class Cube(object):
  def __init__(self, min_x, min_y, min_z, size):
    self.count = -1
    self.min_x = min_x
    self.max_x = min_x + size -1
    self.min_y = min_y
    self.max_y = min_y + size -1 
    self.min_z = min_z
    self.max_z = min_z + size -1
    self.size = size
    self.distance = abs(min_x) + abs(min_y) + abs(min_z)  # distance from the origin

  def __eq__(self, other):
    if self.x != other.x:
      return False
    if self.y != other.y:
      return False
    if self.z != other.z:
      return False
    if self.size != other.size:
      return False
    return True

  def __lt__(self, other):
    if self.count < other.count:
      return True
    if other.count < self.count:
      return False
    if self.distance < other.distance:
      return True
    if other.distance < self.distance:
      return False
    return self.size < other.size

  def __repr__(self):
    return "Cube(%d,%d,%d/%d (%d from orig; %d bots))" % (
      self.min_x, self.min_y, self.min_z, self.size, self.distance, self.count)

  def in_range(self, bot):
    # find the edge of the cube closest to the point
    distance = 0
    if bot.x < self.min_x:
      distance += self.min_x - bot.x
    if bot.x > self.max_x:
      distance += bot.x - self.max_x
    if bot.y < self.min_y:
      distance += self.min_y - bot.y
    if bot.y > self.max_y:
      distance += bot.y - self.max_y
    if bot.z < self.min_z:
      distance += self.min_z - bot.z
    if bot.z > self.max_z:
      distance += bot.z - self.max_z

    if distance <= bot.r:
      return True
    return False

# main
needed = max(max_x - min_x, max_y - min_y, max_z - min_z)
side = 2
while side < needed:
  side *= 2

to_check = [Cube(min_x, min_y, min_z, side)]

while to_check:
  to_check = sorted(to_check)
  #print "Options are", to_check
  cube = to_check.pop()  # highest bots, TODO: confirm
  bot_count = 0
  for bot in bots:
    if cube.in_range(bot):
      bot_count += 1
  cube.count = bot_count
  #print "Chosen cube: %s" % cube
  if cube.size == 1:
    print "We're done."
    print cube.distance
    break

  min_x = cube.min_x
  min_y = cube.min_y
  min_z = cube.min_z
  half = cube.size / 2
  half_x = half + min_x
  half_y = half + min_y
  half_z = half + min_z

  new_cubes = [
    (min_x, min_y, min_z), (min_x, min_y, half_z),
    (min_x, half_y, min_z), (min_x, half_y, half_z),
    (half_x, min_y, min_z), (half_x, min_y, half_z),
    (half_x, half_y, min_z), (half_x, half_y, half_z)
  ]

  for x, y, z in new_cubes:
    new_cube = Cube(x, y, z, half)
    bot_count = 0
    for bot in bots:
      if new_cube.in_range(bot):
        bot_count += 1
    new_cube.count = bot_count
    to_check.append(new_cube)
