#!/usr/bin/env python

from collections import deque

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
  def __init__(self, minx, maxx, miny, maxy, minz, maxz):
    # Actually this is ok. A range of x..x includes only point x.
    #if minx == maxx or miny == maxy or minz == maxz:
    #  print "BUG"
    #  print("Not creating Cuboid(%d, %d, %d, %d, %d, %d)" % (minx, maxx, miny, maxy, minz, maxz))
    #  exit(1)
    self.minx = minx
    self.miny = miny
    self.minz = minz
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz

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
      print("BUG: unexpected value %d" % x)
      exit(1)
    other = Cuboid(x + 1, self.maxx, self.miny, self.maxy, self.minz, self.maxz)
    self.maxx = x
    return other

  def splity(self, y):
    """Splits self. Returns a new cuboid with everything past the split point.
    """
    if y < self.miny or y > self.maxy:
      print("BUG: unexpected value %d" % y)
      exit(1)
    other = Cuboid(self.minx, self.maxx, y + 1, self.maxy, self.minz, self.maxz)
    self.maxy = y
    return other

  def splitz(self, z):
    """Splits self. Returns a new cuboid with everything past the split point.
    """
    if z < self.minz or z > self.maxz:
      print("BUG: unexpected value %d" % z)
      exit(1)
    other = Cuboid(self.minx, self.maxx, self.miny, self.maxy, z + 1, self.maxz)
    self.maxz = z
    return other

  def overlap_x(self, other):
    """If there is any overlap, including one cuboid containing the other, return
       a point at which to split."""
    #print "overlap_x", self, other
    #print(self.minx, self.maxx, other.minx, other.maxx)
    # Self extends to the left of other.
    # Both are checking other's MINIMUM
    if self.minx < other.minx and self.maxx > other.minx: # other's minimum is contained
      #print "exit1"
      return other.minx
      # Self extends to the right of other.
    if self.minx >= other.minx and self.minx <= other.maxx and self.maxx > other.maxx: # self's minimum is contained
      #print "exit2", other.maxx
      return other.maxx
    return None

  def overlap_y(self, other):
    """If there is any overlap, including one cuboid containing the other, return
       a point at which to split."""

    #print "overlap_y", self, other
    if self.miny < other.miny and self.maxy > other.miny: # other's minimum is contained
      #print "exit1", other.miny
      return other.miny
    if self.miny >= other.miny and self.miny <= other.maxy and self.maxy > other.maxy: # self's minimum is contained
      #print "exit2", other.maxy
      return other.maxy
    return None

  def overlap_z(self, other):
    """If there is any overlap, including one cuboid containing the other, return
       a point at which to split."""
    #print "overlap_z", self, other
    if self.minz < other.minz and self.maxz > other.minz: # other's minimum is contained
      return other.minz
    if self.minz >= other.minz and self.minz <= other.maxz and self.maxz > other.maxz: # self's minimum is contained
      return other.maxz
    return None


  def split_if_overlap(self, other):
    """Look for overlaps in multiple places, returning the first split."""
    x = self.overlap_x(other)
    if x:
      #print("Should split x at %d" % x)
      return self.splitx(x)
    y = self.overlap_y(other)
    if y:
      #print("Should split y at %d" % y)
      return self.splity(y)
    z = self.overlap_z(other)
    if z:
      #print("Should split z at %d" % z)
      return self.splitz(z)
    return None

  def same(self, other):
    if (self.minx == other.minx and self.maxx == other.maxx and
        self.miny == other.miny and self.maxy == other.maxy and
        self.minz == other.minz and self.maxz == other.maxz):
      return True
    return False
 
  def __repr__(self):
    return "(x=%d..%d,y=%d..%d,z=%d..%d)" % (self.minx, self.maxx, self.miny,
                                             self.maxy, self.minz, self.maxz)

class CuboidGroup(object):
  def __init__(self, name, cuboid, action):
    self.name = name
    self.cuboids = [cuboid]
    self.action = action

def dedupe(groups):
  found = False
  for i in range(len(groups)):
    group = groups[i]
    action = group.action
    print("\n\nStarting group %d of %s" % (i, len(groups)))
    to_check = deque(group.cuboids)
    while to_check:
      #print("%d groups to check in here" % len(to_check))
      cuboid = to_check.pop()
      #print("*** Checking %s" % cuboid)
      # check against every other group
      for j in range(0, i):
        othergroup = groups[j] # only looking at the ones we've already passed
        if group.action == othergroup.action:
          continue  # don't need to change it so who cares
      #for othergroup in groups:
      # Next steps
      # TODO: if doing it this way, need to split othergroup here too if needed
      # TODO: also cover the case where one group subsumes another

        #print ("Checking group %d: %s" % (othergroup.name, othergroup.cuboids))
        if group == othergroup:
          continue
        for other in othergroup.cuboids:
          #print("Self: %s, Other: %s" % (cuboid, other))
          if cuboid.same(other):
            continue
          while True:
            split = cuboid.split_if_overlap(other)
            if split:
              #print("Splitting into %s and %s" % (cuboid, split))
              group.cuboids.append(split)
              to_check.append(split)
              to_check.append(cuboid) # check it again
              found = True
            else:
              break
      # when we leave here, nothing in this group should have remaining places it can helpfully split
  return found

groups =  []
for i in range(0, len(lines)):
  line = lines[i]
  onoff, coords = line.split()
  x,y,z = coords.split(",")
  minx, maxx = [int(x) for x in x.split("=")[1].split("..")]
  miny, maxy = [int(x) for x in y.split("=")[1].split("..")]
  minz, maxz = [int(x) for x in z.split("=")[1].split("..")]
  if onoff == "on":
    action = 1
  else:
    action = 0
  group = CuboidGroup(i, Cuboid(minx, maxx, miny, maxy, minz, maxz), action)
  groups.append(group)

i = 0
while True:
  found = dedupe(groups)
  i += 1
  if not found:
    break
print("Finished removing overlaps after %d iterations." % i)
