#!/usr/bin/env python
# Advent of code Day 10.
# Has an off by one error somewhere.
# Don't use this for vaporizing real asteroids.

import sys

class Asteroid(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.name = "%s_%s" % (x, y)
    self.yes = set()
    self.no = set()
    self.no.add(self)
    self.maybe = set()
    self.direction = None
    self.slope = -999999999
    self.distance = -9999999999
    self.alive = True

  def set_context(self, direction, slope, distance):
    # Where is this thing in relation to the station
    self.direction = direction
    self.slope = slope
    self.distance = distance

  def __lt__(self, other):
    """For sorting."""
    weight = {"up": 1, "right":2, "down":3, "left":4}
    if weight[self.direction] < weight[other.direction]:
      return True
    if weight[self.direction] > weight[other.direction]:
      return False
    if self.slope < other.slope:
      return True
    if self.slope > other.slope:
      return False
    return self.distance < other.distance

  def __repr__(self):
    return "[%s] %s %f %d (%d)" % (
      self.name, self.direction, self.slope, self.distance,
      self.x * 100 + self.y)

# main
with open("input.txt", "r") as f:
  lines = f.readlines()


#lines = [".#..#", ".....", "#####", "....#", "...##"]
#lines = [".#....#####...#..",
#"##...##.#####..##", "##...#...#.#####.",
#"..#.....#...###..", "..#.#.....#....##"]

print "Read %d lines of length %d" % (len(lines), len(lines[0]))
asteroids = {}

height = len(lines)
width = len(lines[0].strip())

for y in range (0, height):
  line = lines[y].strip()
  s = "%s" % y
  for x in range (0, len(line)):
    s += line[x]
    if line[x] == "#":
      asteroid = Asteroid(x, y)
      asteroids[asteroid.name] = asteroid
  print s

print "Found %d asteroids" % len(asteroids)

for station in asteroids.values():
  # get everything in thr same horizontal line
  blocked = False
  for i in range (station.x -1, -1, -1):
    try:
      b = asteroids["%s_%s" % (i, station.y)]
      if not blocked:
        station.yes.add(b)
        #print b.name, "is not blocked"
        blocked = True
      else:
        #print b.name, "is blocked"
        station.no.add(b)
    except KeyError:
      continue
  blocked = False

  for i in range (station.x + 1, width + 1):
    try:
      b = asteroids["%s_%s" % (i, station.y)]
      if not blocked:
        station.yes.add(b)
        #print b.name, "is not blocked"
        blocked = True
      else:
        station.no.add(b)
        #print b.name, "is blocked"
    except KeyError:
      continue

  # get everything in the same vertical line
  blocked = False
  for i in range (station.y -1, -1, -1):
    try:
      b = asteroids["%s_%s" % (station.x, i)]
      if not blocked:
        station.yes.add(b)
        #print b.name, "is not blocked"
        blocked = True
      else:
        #print b.name, "is blocked"
        station.no.add(b)
    except KeyError:
      continue
  blocked = False

  for i in range (station.y + 1, height + 1):
    try:
      b = asteroids["%s_%s" % (station.x, i)]
      if not blocked:
        station.yes.add(b)
        #print b.name, "is not blocked"
        blocked = True
      else:
        station.no.add(b)
        #print b.name, "is blocked"
    except KeyError:
      continue

  # Now diagonals
  count = len(asteroids)
  slopes = {}
  for node in asteroids.values():
    if node in station.no:
      continue
    if node in station.yes:
      continue
    rise = (station.y - node.y) * 1.0
    run = (station.x - node.x) * 1.0
    slope = (rise / run, station.x < node.x)  # slope and a bool to show which side it is
    if slope in slopes:
      existing_node = slopes[slope]
      existing_node_distance = existing_node.x - station.x + existing_node.y - station.y
      this_node_distance = node.x - station.x + node.y - station.y
      if this_node_distance < existing_node_distance:
        station.no.add(existing_node)
        slopes[slope] = node
      else:
        station.no.add(node)
    else:
      slopes[slope] = node
  for node in slopes.values():
    station.yes.add(node)

highest = 0
chosen = None
for station in asteroids.values():
  if len(station.yes) > highest:
    highest = len(station.yes)
    chosen = station
print highest, chosen

# Part 2
station = asteroids["19_14"]
#station = asteroids["11_13"]
slopes = {}  # slope, [nodes]

del asteroids[station.name]

nodes = asteroids.values()
for node in nodes:
  if node == station:
    print "nope"
    sys.exit(0)

  rise = (station.y - node.y) * 1.0
  run = (station.x - node.x) * 1.0
  if run == 0 and station.x > node.x:  # straight down
    slope = float("inf")
    direction = "down"
  elif run == 0:
    slope = float("inf")
    direction = "up"
  else:
    if station.x < node.x:
      direction = "right"
    else:
      direction = "left"
    slope = rise / run
  distance = abs(rise) + abs(run)
  node.set_context(direction, slope, distance)

ordered = sorted(nodes)

count = 0
while len(asteroids) > 0:
  last_slope = -999999999
  last_direction = "nowhere"
  for node in ordered:
    if node.slope == last_slope and node.direction == last_direction:
      continue # keep moving clockwise
    if node.name not in asteroids: # already vaporised
      continue
    last_slope = node.slope
    last_direction = node.direction
    count += 1
    print count, node
    del asteroids[node.name]

