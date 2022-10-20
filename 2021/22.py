#!/usr/bin/env python

from collections import deque


class Cuboid(object):
  # min and max are inclusive
  def __init__(self, minx, maxx, miny, maxy, minz, maxz):
    self.minx = minx
    self.miny = miny
    self.minz = minz
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz
    self.on = False # default

  def volume(self):
    return ((self.maxx + 1 - self.minx) * (self.maxy + 1 - self.miny) *
            (self.maxz + 1 - self.minz))


  def overlap(self, other):
    """Return the cuboid that describes the overlap between this cuboid and
    another.

    Args:
      other: (Cuboid) the thing that might overlap.
    Returns:
      (Cuboid): a new cuboid describing the overlap. And even though nobody will
                ever care about scoping or GCing this object I feel such an urge to
                write "caller takes ownership".
    """

    (minx1, maxx1, miny1, maxy1, minz1, maxz1) = (self.minx, self.maxx,
         self.miny, self.maxy, self.minz, self.maxz)
    (minx2, maxx2, miny2, maxy2, minz2, maxz2) = (other.minx, other.maxx,
         other.miny, other.maxy, other.minz, other.maxz)

    #print("Self: minx:%s, maxx:%s" % (minx1, maxx1))
    #print("Other: minx:%s, maxx:%s" % (minx2, maxx2))

    if minx2 > maxx1 or miny2 > maxy1 or minz2 > maxz1:
      return None

    if minx1 > maxx2 or miny1 > maxy2 or minz1 > maxz2:
      return None

    # So it's overlapping.
    # The overlap starts on the X axis at the maximum of the two coordinates
    # minx1 and minx2 and ends at the minimum of maxx1 and maxx2
    minx = max(minx1, minx2)
    maxx = min(maxx1, maxx2)
    miny = max(miny1, miny2)
    maxy = min(maxy1, maxy2)
    minz = max(minz1, minz2)
    maxz = min(maxz1, maxz2)

    return Cuboid(minx, maxx, miny, maxy, minz, maxz)

  def subtract_all(self, to_remove):
    """Remove a set of cuboids from this one, splitting this one into
       multiple pieces if needed. Return the pieces."""
    # Algorithm:
    remaining = [self] # TODO: replace this

    return remaining


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


  def same(self, other):
    if (self.minx == other.minx and self.maxx == other.maxx and
        self.miny == other.miny and self.maxy == other.maxy and
        self.minz == other.minz and self.maxz == other.maxz):
      return True
    return False
 
  def __repr__(self):
    return "(x=%d/%d,y=%d/%d,z=%d/%d)" % (self.minx, self.maxx, self.miny,
                                          self.maxy, self.minz, self.maxz)

inputfile = "input22.txt"
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

def testsmall():
  lines = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".split("\n")
  return lines



def create(lines):
  cuboids = []
  for i in range(0, len(lines)):
    line = lines[i]
    onoff, coords = line.split()
    x,y,z = coords.split(",")
    minx, maxx = [int(x) for x in x.split("=")[1].split("..")]
    miny, maxy = [int(x) for x in y.split("=")[1].split("..")]
    minz, maxz = [int(x) for x in z.split("=")[1].split("..")]
    if onoff == "on":
      is_on = True
    elif onoff == "off":
      is_on = False
    else:
      print("Error: onoff is %s" % onoff)
      exit()
    newboid = Cuboid(minx, maxx, miny, maxy, minz, maxz)
    newboid.on = is_on
    cuboids.append(newboid)
  return cuboids



def test():
  lines = testsmall()
  cuboids = create(lines)

  newboid = cuboids[0].overlap(cuboids[1])
  assert(newboid.volume() == 8)
  newboid = cuboids[1].overlap(cuboids[0])
  assert(newboid.volume() == 8)

  newboid = cuboids[0].overlap(cuboids[2])
  assert(newboid.volume() == 8)
  newboid = cuboids[2].overlap(cuboids[0])
  assert(newboid.volume() == 8)

  newboid = cuboids[0].overlap(cuboids[3])
  assert(newboid.volume() == 1)
  newboid = cuboids[3].overlap(cuboids[0])
  assert(newboid.volume() == 1)

  newboid = cuboids[1].overlap(cuboids[3])
  assert(not newboid)
  newboid = cuboids[3].overlap(cuboids[1])
  assert(not newboid)

  newboid = cuboids[2].overlap(cuboids[3])
  assert(newboid.volume() == 1)
  newboid = cuboids[3].overlap(cuboids[2])
  assert(newboid.volume() == 1)

  print ("PASS")

#test()

on_cuboids = set()
lines = testsmall()[0:4]
print (lines)
cuboids = create(lines)

# Algorithm:
for cuboid in cuboids:
  print("On:", on_cuboids)
  print("Now looking at", cuboid)
  # if we're turning on new points
  #   compare it with every existing on_cuboid, find each overlap
  #   store all the overlaps until the end of the loop
  if cuboid.on:
    overlaps = []
    for on in on_cuboids:
      overlap = cuboid.overlap(on)
      if overlap:
        overlaps.append(overlap)
    print ("On overlaps:", overlaps)
#   then cycle through the overlaps, subtracting each one from this cuboid (or its
#   successors)
    replacementoids = cuboid.subtract_all(overlaps)
#   whatever is left (i.e., not already on by another cuboid), add to on_cuboids
    on_cuboids.update(replacementoids)
  else:
# else if we're turning points off
#   compare it with every on_cuboid, find each overlap
    new_on_cuboids = set()
    while on_cuboids:
      on = on_cuboids.pop()
      overlap = cuboid.overlap(on)
      print ("Off overlap:", overlap)
      if overlap:
        # if there's an overlap, subtract the overlap from that on_cuboid
        # i.e., turn those points off
        # do that by creating up to six new on_cuboids and discarding the original
        replacementoids = on.subtract_all(cuboid)
        new_on_cuboids.update(replacementoids)
      else:
        new_on_cuboids.add(on)
    on_cuboids = new_on_cuboids

