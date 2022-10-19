#!/usr/bin/env python

# Naive solution to part 1, knowing well it won't work for part 2.

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

#lines = test()

class Cuboid(object):
  def __init__(self, minx, maxx, miny, maxy, minz, maxz, onoff):
    self.minx = minx
    self.miny = miny
    self.minz = minz
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz
    self.on = onoff
    self.add_bounds()

  def add_bounds(self):
    if self.minx < -50:
      self.minx = -50
    if self.miny < -50:
      self.miny = -50
    if self.minz < -50:
      self.minz = -50
    if self.maxx > 50:
      self.maxx = 50
    if self.maxy > 50:
      self.maxy = 50
    if self.maxz > 50:
      self.maxz = 50

  def points(self):
    """Returns all of the points in a cuboid"""
    to_return = []
    for x in range(self.minx, self.maxx + 1):
      for y in range(self.miny, self.maxy + 1):
        for z in range(self.minz, self.maxz + 1):
          to_return.append((x, y, z))
    return to_return

  def __repr__(self):
    return "(x=%d..%d,y=%d..%d,z=%d..%d)" % (self.minx, self.maxx, self.miny,
                                             self.maxy, self.minz, self.maxz)
cuboids =  []
on_cubes = set()
for i in range(0, len(lines)):
  line = lines[i]
  onoff, coords = line.split()
  x,y,z = coords.split(",")
  minx, maxx = [int(x) for x in x.split("=")[1].split("..")]
  miny, maxy = [int(x) for x in y.split("=")[1].split("..")]
  minz, maxz = [int(x) for x in z.split("=")[1].split("..")]
  if onoff == "on":
    on = True
  elif onoff == "off":
    on = False
  else:
    print("Error: onoff is %s" % onoff)
    exit()
  cuboids.append(Cuboid(minx, maxx, miny, maxy, minz, maxz, on))

for c in cuboids:
  on = c.on
  if on:
    for p in c.points():
      on_cubes.add(p)
  else:
    for p in c.points():
      if p in on_cubes:
        on_cubes.remove(p)


print (len(on_cubes))
