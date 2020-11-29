#!/usr/bin/env python
# Advent of code day 11.


class Node(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.edges = []

with open("input11.txt", "r") as f:
  moves = f.read().strip().split(",")

def walk(moves):
  x = 0
  y = 0
  longest = 0
# north is negative
  for move in moves:
    if move == "n":
      y -= 1
    elif move == "ne":
      x += 1
      y -= 0.5
    elif move == "se":
      x += 1
      y += 0.5
    elif move == "s":
      y += 1
    elif move == "sw":
      x -= 1
      y += 0.5
    elif move == "nw":
      x -= 1
      y -= 0.5
    distance = find((x, y))
    if distance > longest:
      longest = distance
  return (x, y), longest

def find(xxx_todo_changeme):
  (ex, ey) = xxx_todo_changeme
  sx, sy = 0, 0

  steps = 0
  while (ex, ey) != (sx, sy):
    if ex == sx:
      # just need to move on the y axis
      if sy > ey:
        sy -= 1 # go north
      else:
        sy += 1 # go south
    elif ey == sy:
      # just need to move on the x axis
      if sx > ex:
        sx -= 1 # go west
      else:
        sx += 1 # go east
    else:
      # x and y are both different
      if sx > ex and sy > ey:
        sx -= 1; sy -= 0.5  # go northwest
      elif sx > ex and sy < ey:
        sx -= 1; sy += 0.5  # go southwest
      elif sx < ex and sy > ey:
        sx += 1; sy -= 0.5  # go northeast
      elif sx < ex and sy < ey:
        sx += 1; sy += 0.5  # go southeast
      else:
        print("we have a bug?")
        exit()
    steps += 1
  return steps

assert walk(["ne","ne","sw","sw"])[0] == (0, 0)

assert find(walk(["se","sw","se","sw","sw"])[0]) == 3
assert find(walk(["ne","ne","s","s"])[0]) == 2
assert find(walk(["ne","ne","sw","sw"])[0]) == 0
assert find(walk(["ne","ne", "ne"])[0]) == 3

coord, distance = walk(moves)

print("Part 1:", find(coord))
print("Part 2:", distance)
