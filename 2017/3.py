#!/usr/bin/env python
# Advent of code Day 3.

class Coord(object):
  def __init__(self, name, x, y):
    self.name = str(name).zfill(2)
    self.x = x
    self.y = y

  def __repr__(self):
    return "%s: (%d,%d)" % (self.name, self.x, self.y)

n = 277678  # input value

radius = 0
location = 1
x = 0
y = 0

# for drawing
coords = {}

# for solving part 1
squares = {}

# for solving part 2
totals = {}

largest = -1

def set_value(x, y, value):
  coords[(x, y)] = Coord(value, x, y)
  squares[value] = coords[(x, y)]

  if value == 0:  # special case for the first square
    totals[(x, y)] = 1
    return

  directions = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),  (0, 0),  (0, 1),
                (1, -1), (1, 0), (1, 1)]
  total = 0
  for direction in directions:
    check_x = x + direction[0]
    check_y = y + direction[1]
    if (check_x, check_y) in totals:
      total += totals[(check_x, check_y)]
  totals[(x, y)] = total
  return total

set_value(0, 0, 0)


while location <= n:

  radius += 1
  # move right <radius> times
  for i in range(radius):
    location += 1
    x += 1
    total = set_value(x, y, location)
    if total > n and largest < 0:
      largest = total

  # move up radius times
  for i in range(radius):
    location += 1
    y -= 1  # up is lower
    total = set_value(x, y, location)
    if total > n and largest < 0:
      largest = total

  radius += 1
  # move left radius times
  for i in range(radius):
    location += 1
    x -= 1
    total = set_value(x, y, location)
    if total > n and largest < 0:
      largest = total

  # move down radius times
  for i in range(radius):
    location += 1
    y += 1  # up is lower
    total = set_value(x, y, location)
    if total > n and largest < 0:
      largest = total




for y in range(-5, 5):
  s = ""
  for x in range (-5, 5):
    if (x, y) in coords:
      s += coords[(x,y)].name
      s += " "
    else:
      s += ".. "
  print s

print "Part 1"
print squares[n]
print squares[n].x + squares[n].y

print "Part 2"

for y in range(-3, 3):
  s = ""
  for x in range (-3, 3):
    if (x, y) in totals:
      s += str(totals[(x,y)]).zfill(5)
      s += " "
    else:
      s += ".. "
  print s

print largest
