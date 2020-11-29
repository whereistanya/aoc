#!/usr/bin/env python
# Advent of code Day 25

class Constellation(object):
  def __init__(self, point):
    x, y, z, a = point
    self.max_x = x
    self.min_x = x
    self.max_y = y
    self.min_y = y
    self.max_z = z
    self.min_z = z
    self.max_a = a
    self.min_a = a
    self.stars = set()

  def __repr__(self):
    s = "Constellation:(%d-%d),(%d-%d),(%d-%d)-(%d-%d)" % (
      self.min_x, self.max_x, self.min_y, self.max_y,
      self.min_z, self.max_z, self.min_a, self.max_a)
    return s

  def connected(self, point):
    x, y, z, a = point
    distance = 0
    if x > self.max_x:
      distance += (x - self.max_x)
    if x < self.min_x:
      distance += (self.min_x - x)
    if y > self.max_y:
      distance += (y - self.max_y)
    if y < self.min_y:
      distance += (self.min_y - y)
    if z > self.max_z:
      distance += (z - self.max_z)
    if z < self.min_z:
      distance += (self.min_z - z)
    if a > self.max_a:
      distance += (a - self.max_a)
    if a < self.min_a:
      distance += (self.min_a - a)

    max_connected = False
    if distance <= 3:
      max_connected = True
    star_connected = False
    for star in self.stars:
      if point == star:
        continue
      star_x, star_y, star_z, star_a = star
      if (abs(star_x - x) + abs(star_y - y) + abs(star_z - z) + abs(star_a - a)) <= 3:
        star_connected = True
    if star_connected != max_connected:
      print("Ok, the range assumption doesn't work")
    return star_connected

  def insert(self, point):
    self.stars.add(point)
    x, y, z, a = point
    if x > self.max_x:
      self.max_x = x
    if x < self.min_x:
      self.min_x = x
    if y > self.max_y:
      self.max_y = y
    if y < self.min_y:
      self.min_y = y
    if z > self.max_z:
      self.max_z = z
    if z < self.min_z:
      self.min_z = z
    if a > self.max_a:
      self.max_a = a
    if a < self.min_a:
      self.min_a = a

  def extend(self, other):
    for star in other.stars:
      self.stars.add(star)
    if other.max_x > self.max_x:
      self.max_x = other.max_x
    if other.min_x < self.min_x:
      self.min_x = other.min_x
    if other.max_y > self.max_y:
      self.max_y = other.max_y
    if other.min_y < self.min_y:
      self.min_y = other.min_y
    if other.max_z > self.max_z:
      self.max_z = other.max_z
    if other.min_z < self.min_z:
      self.min_z = other.min_z
    if other.max_a > self.max_a:
      self.max_a = other.max_a
    if other.min_a < self.min_a:
      self.min_a = other.min_a

def make_constellations(lines):
  points = set()
  constellations = set()
  for line in lines:
    x,z,y,a = line.strip().split(",")
    points.add((int(x),int(y),int(z),int(a)))

  for point in points:
    matched = []
    for constellation in constellations:
      if constellation.connected(point):
        matched.append(constellation)

    if len(matched) == 0:
      new_constellation = Constellation(point)
      new_constellation.stars.add(point)
      constellations.add(new_constellation)
    elif len(matched) == 1:
      matched[0].insert(point)
    else:
      main_constellation = matched[0]
      for i in range(1, len(matched)):
        other_constellation = matched[i]
        main_constellation.extend(other_constellation)
        constellations.remove(other_constellation)
        main_constellation.insert(point)

  return constellations

lines1 = [
   "0,0,0,0",
   "3,0,0,0",
   "0,3,0,0",
   "0,0,3,0",
   "0,0,0,3",
   "0,0,0,6",
   "9,0,0,0",
  "12,0,0,0",
]

lines2 = [
  "-1,2,2,0",
  "0,0,2,-2",
  "0,0,0,-2",
  "-1,2,0,0",
  "-2,-2,-2,2",
  "3,0,2,-1",
  "-1,3,2,2",
  "-1,0,-1,0",
  "0,2,1,-2",
  "3,0,0,0",
]

lines3 = [
  "1,-1,0,1",
  "2,0,-1,0",
  "3,2,-1,0",
  "0,0,3,1",
  "0,0,-1,-1",
  "2,3,-2,0",
  "-2,2,0,0",
  "2,-2,0,-1",
  "1,-1,0,-1",
  "3,2,0,2",
]

lines4 = [
  "1,-1,-1,-2",
  "-2,-2,0,1",
  "0,2,1,3",
  "-2,3,-2,1",
  "0,2,3,-2",
  "-1,-1,1,-2",
  "0,-2,-1,0",
  "-2,2,3,-1",
  "1,2,2,0",
  "-1,-2,0,-2",
]
with open("day25input.txt", "r") as f:
  lines = f.readlines()

assert len(make_constellations(lines1)) == 2
assert len(make_constellations(lines2)) == 4
assert len(make_constellations(lines3)) == 3
assert len(make_constellations(lines4)) == 8

print(len(make_constellations(lines)))
