#!/usr/bin/env python3

import sys
import util.grid as g

test = True
test = False

if test:
  filename = "test24.txt"
else:
  filename = "input24.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

class Wind(object):
  def __init__(self, point):
    self.location = (point.x, point.y)
    self.direction = point.value
    self.grid = grid
    # 0 is wall
    self.minx = 1
    self.miny = 1
    # maxx is the actual biggest non-wall, not the upper bound for ranges
    self.maxx = self.grid.maxx - 2
    self.maxy = self.grid.maxy - 2

  def __repr__(self):
    return "Wind(dir %s loc %s)" % (self.direction, self.location)

  def move(self):
    x, y = self.location
    if self.direction == ">":
      if x + 1 > self.maxx:
        x = self.minx
      else:
        x = x + 1
    elif self.direction == "<":
      if x - 1 < self.minx:
        x = self.maxx
      else:
        x = x - 1
    elif self.direction == "^":
      if y - 1 < self.miny:
        y = self.maxy
      else:
        y = y - 1
    elif self.direction == "v":
      if y + 1 > self.maxy:
        y = self.miny
      else:
        y = y + 1
    self.location = (x, y)
    return (x, y)

grid = g.Grid(lines)


winds = []
for symbol in [">", "<", "^", "v"]:
  winds.extend(
    [Wind(location) for location in grid.get_by_char(symbol)])
print(winds)



# Just using the grid locations as a way of drawing pictures. Don't
# want fully functional points recorded, just characters.
for k, v in grid.grid.items():
  grid.grid[k] = v.value

grid.printraw()

ingate = None
outgate = None
for i in range(len(lines[0])):
  if lines[0][i] == ".":
    ingate = (i, 0)
    break

for i in range(len(lines[-1])):
  if lines[-1][i] == ".":
    outgate = (i, len(lines) - 1)
    break

print(ingate, outgate)


def get_neighbours(point):
  x, y = point
  neighbours = []
  to_add = [ (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
  for neighbour in to_add:
    neighbours.append(neighbour)
  return neighbours


found = False
minute = 0
possible_locations = set([ingate])
while True:
  if found:
    break
  #print("Minute %d locations %s" % (minute, len(possible_locations)))
  new_grid = {}
  for wind in winds:
    #print("moving", wind)
    new_location = wind.move()
    new_grid[new_location] = wind.direction
  to_check = set(possible_locations)

  possible_locations.clear()
  while to_check:
    start = to_check.pop()
    if start == outgate:
      print("Turning around at minute", minute)
      found = True
      break
    if start not in new_grid:
      possible_locations.add(start) # don't move
    neighbours = get_neighbours(start)
    for n in neighbours:
      if n not in grid.grid:
        continue
      if n in new_grid:
        continue
      if n in grid.grid and grid.grid[n] == "#":
        continue
      possible_locations.add(n)
  minute += 1

possible_locations = set([outgate])
found = False
while True:
  if found:
    break
  #print("Minute %d locations %s" % (minute, len(possible_locations)))
  new_grid = {}
  for wind in winds:
    #print("moving", wind)
    new_location = wind.move()
    new_grid[new_location] = wind.direction
  to_check = set(possible_locations)

  possible_locations.clear()
  while to_check:
    start = to_check.pop()
    if start == ingate:
      print("Back home at minute", minute)
      found = True
      break
    if start not in new_grid:
      possible_locations.add(start) # don't move
    neighbours = get_neighbours(start)
    for n in neighbours:
      if n not in grid.grid:
        continue
      if n in new_grid:
        continue
      if n in grid.grid and grid.grid[n] == "#":
        continue
      possible_locations.add(n)
  minute += 1


possible_locations = set([ingate])
found = False
while True:
  if found:
    break
  #print("Minute %d locations %s" % (minute, len(possible_locations)))
  new_grid = {}
  for wind in winds:
    #print("moving", wind)
    new_location = wind.move()
    new_grid[new_location] = wind.direction
  to_check = set(possible_locations)

  possible_locations.clear()
  while to_check:
    start = to_check.pop()
    if start == outgate:
      print("Finished at minute", minute)
      found = True
      break
    if start not in new_grid:
      possible_locations.add(start) # don't move
    neighbours = get_neighbours(start)
    for n in neighbours:
      if n not in grid.grid:
        continue
      if n in new_grid:
        continue
      if n in grid.grid and grid.grid[n] == "#":
        continue
      possible_locations.add(n)
  minute += 1
