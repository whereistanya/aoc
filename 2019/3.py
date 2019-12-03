#!/usr/bin/env python
# Advent of code Day 1.

import math

def up(x, y, n):
  points = []
  i = y
  while i <= y + n:
    points.append((x, i))
    i += 1
  return points

def down(x, y, n):
  points = []
  i = y
  while i >= y - n:
    points.append((x, i))
    i -= 1
  return points

def right(x, y, n):
  points = []
  i = x
  while i <= x + n:
    points.append((i, y))
    i += 1
  return points


def left(x, y, n):
  points = []
  i = x
  while i >= x - n:
    points.append((i, y))
    i -= 1
  return points


def lowest_distance(a, b, part=1):
  lineA = a.strip().split(",")
  lineB = b.strip().split(",")
  funcs = { "U": up, "D": down, "R": right, "L": left }

  pointsA = {}
  pointsB = {}
  x = 0
  y = 0
  step = 0
  for coord in lineA:
    coord.strip()
    d = funcs[coord[0]]
    n = int(coord[1:])
    for point in d(x, y, n):
      if point in pointsA:
        continue
      pointsA[point] = step
      step += 1
      x = point[0]
      y = point[1]


  x = 0
  y = 0
  step = 0
  for coord in lineB:
    coord.strip()
    d = funcs[coord[0]]
    n = int(coord[1:])
    for point in d(x, y, n):
      if point in pointsB:
        continue
      pointsB[point] = step
      step += 1
      x = point[0]
      y = point[1]

  crosses = pointsA.viewkeys() & pointsB.viewkeys()
  crosses.remove((0,0))
  lowest = 99999999999

  for cross in crosses:
    if part == 1:
      distance = abs(cross[0]) + abs(cross[1])
    else:
      # haha input validation
      distance = pointsA[cross] + pointsB[cross]
    if distance < lowest:
      lowest = distance
  return lowest


assert lowest_distance("R8,U5,L5,D3", "U7,R6,D4,L4", 1) == 6
assert lowest_distance(
  "R75,D30,R83,U83,L12,D49,R71,U7,L72",
  "U62,R66,U55,R34,D71,R55,D58,R83", 1) == 159
assert lowest_distance(
  "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
  "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 1) == 135

with open("input.txt", "r") as f:
  lines = f.readlines()
  assert len(lines) == 2
  print lowest_distance(lines[0], lines[1], 1)
  print lowest_distance(lines[0], lines[1], 2)
