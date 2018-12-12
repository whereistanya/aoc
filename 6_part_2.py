#!/usr/bin/env python
# Advent of code Day 6 part 2. 3 nested loops seriously? yes but it works?

with open("day6input.txt", "r") as f:
  lines = f.readlines()

######################################
# Part two
######################################

"""
lines = [
  "1, 1",
  "1, 6",
  "8, 3",
  "3, 4",
  "5, 5",
  "8, 9"
]
"""

class Coord(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Location(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.total = 0

coords = []  # [Coord, ...]

min_x = 99999
max_x = 0
min_y = 99999
max_y = 0

for line in lines:
  x, y = line.strip().split(", ")
  x = int(x)
  y = int(y)
  if x > max_x:
    max_x = x
  if x < min_x:
    min_x = x
  if y > max_y:
    max_y = y
  if y < min_y:
    min_y = y
  coords.append(Coord(x, y))

locations = []

for i in range (min_x, max_x):
  for j in range (min_y, max_y):
    location = Location(i, j)
    for coord in coords:
      # distance from i, j to coord
      distance = abs(coord.x - i) + abs(coord.y - j)
      location.total += distance
    locations.append(location)

count = 0
for location in locations:
  if location.total < 10000:
    count += 1

print count
