#!/usr/bin/env python

from collections import dequeue

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test():
  lines = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".split("\n")
  return lines

lines = test()

class Cuboid(object):
  def __init__(self, minx, maxx, miny, maxy, minz, maxz, action):
    self.minx = minx
    self.miny = miny
    self.minz = minz
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz
    self.action = action

  def contains(self, other):
    if self.maxx < other.maxx:
      return False
    if self.maxy < other.maxy:
      return False
    if self.maxz < other.maxz:
      return False
    if self.minx > other.minx:
      return False
    if self.miny > other.miny:
      return False
    if self.minz > other.minz:
      return False
    # other fits inside self
    return True


  def splitx(self, x):
    """Splits self. Returns a new cuboid with everything past the split point.
    """
    if x < self.minx or x > self.maxx:
      return None
    other = Cuboid(x, self.maxx, self.miny, self.maxy, self.minz, self.maxz,
                   self.action)
    self.maxx = x
    return other

  def splity(self, y):
    """Splits self. Returns a new cuboid with everything past the split point.
    """
    if y < self.miny or y > self.maxy:
      return None
    other = Cuboid(self.minx, self.maxx, y, self.maxy, self.minz, self.maxz,
                   self.action)
    self.maxz = z
    return other

  def splitz(self, z):
    """Splits self. Returns a new cuboid with everything past the split point.
    """
    if x < self.minz or x > self.maxz:
      return None
    other = Cuboid(self.minx, self.maxx, self.miny, self.maxy, z, self.maxz,
                   self.action)
    self.maxz = z
    return other

  def overlap_x(self, other):
    """If there is any overlap, including one cuboid containing the other, return
       a point at which to split."""
    if self.minx < other.minx and self.maxx > other.minx: # other's minimum is contained
      return other.minx
    if self.minx > other.minx and self.minx < other.maxx: # self's minimum is contained
      return other.maxx

    # TODO: other overlap

  def split_if_overlap(self, other):
    """Look for overlaps in multiple places, returning the first split."""
    x = self.overlap_x(other)
    if x:
      return self.splitx(x)
    y = self.overlap_y(other)
    if y:
      return self.splity(y)
    z = self.overlap_z(other)
    if z:
      return self.splitz(z)
    return None

  def same(self, other):
    """Doesn't compare actions."""
    if (self.minx == other.minx and self.maxx == other.maxx and
        self.miny == other.miny and self.maxy == other.maxy and
        self.minz == other.minz and self.maxz == other.maxz):
      return True


cuboids = dequeue()
for line in lines:
  onoff, coords = line.split()
  x,y,z = coords.split(",")
  minx, maxx = x.split("=")[1].split("..")
  miny, maxy = y.split("=")[1].split("..")
  minz, maxz = z.split("=")[1].split("..")
  if onoff == "on":
    action = 1
  else:
    action = 0
  cuboid = Cuboid(minx, maxx, miny, maxy, minz, maxz, action)

for cuboid in cuboids:
  to_check = deque(cuboids) # compare everything against everything
  while (to_check):
    other = to_check.pop()
    if cuboid.same(other):  # either itself or something occupying the same
                            #space
      continue
    # to maintain the place in the queue, can only split self, not other
    # so perform any splits that reduce overlap
    found = False
    while True:
      split = cuboid.split_if_overlap(other)
      if split:
        found = True
        cuboids.push_left(split) # split might have overlaps of its own
      if not found:
        break
  # when we leave here, cuboid should have no remaining places it can helpfully split


