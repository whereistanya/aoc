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
    self.deleted = False

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
      return self.splitx(x), None
    y = self.overlap_y(other)
    if y:
      #print("Should split y at %d" % y)
      return self.splity(y), None
    z = self.overlap_z(other)
    if z:
      #print("Should split z at %d" % z)
      return self.splitz(z), None
    x = other.overlap_x(self)
    if x:
      #print("Should split x at %d" % x)
      return None, other.splitx(x)
    y = other.overlap_y(self)
    if y:
      #print("Should split y at %d" % y)
      return None, other.splity(y)
    z = other.overlap_z(self)
    if z:
      #print("Should split z at %d" % z)
      return None, other.splitz(z)
    return None, None

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
  # algorithm:
  # place the first group of cuboids (which will contain 1)
  # for each of the second group, if it overlaps with something in the
  # first group, split something, either group. If a cuboid completely
  # overwrites an old cuboid, delete the old one.
  # we don't iterate through the real groups, we make a copy.

  for i in range(len(groups)):
    group = groups[i]
    action = group.action
    print("\n\nStarting group %d of %s" % (i, len(groups)))
    to_place = deque(group.cuboids)
    while to_place:
      cuboid = to_place.pop()
      print("*** Placing %s" % cuboid)

      # check against every other group
      for othergroup in groups[0:i]: # grab a copy of the groups placed so far.
                                   # Some of them may change in this round.
        othercuboids = deque(othergroup.cuboids)
        while othercuboids:
          #print("Checking against %s" % len(othercuboids))
          other = othercuboids.pop()
          if other.deleted:
            continue
          if cuboid.same(other):
            other.deleted = True
            print ("They're the same cuboid.")
            continue
          added_self = []
          added_other = []
          while True:
            split_self, split_other = cuboid.split_if_overlap(other)
            if split_self:
              print("Splitting self into %s and %s" % (cuboid, split_self))
              added_self.append(split_self)
              to_place.appendleft(split_self) # do it next
            elif split_other:
              print("Splitting other into %s and %s" % (cuboid, split_other))
              added_other.append(split_other)
              othercuboids.appendleft(split_other) # do it next
            else:
              print("Adding", added_self, added_other )
              group.cuboids.extend(added_self)
              othergroup.cuboids.extend(added_other)
              break

        #print ("Checking group %d: %s" % (othergroup.name, othergroup.cuboids))
        #print("Self: %s, Other: %s" % (cuboid, other))


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

dedupe(groups)

#print ("Second run should be empty...\n\n\n")
#dedupe(groups)

for group in groups:
  print ("*** %s (%s)" % (group.name, group.action))
  for cuboid in group.cuboids:
    print (cuboid)
    if cuboid.deleted:
      print ("deleted")
