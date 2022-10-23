#!/usr/bin/env python3

from collections import deque

# Turn on add_bounds in the Cuboid class for part 1

class Cuboid(object):
  # from min to max-1 inclusive
  def __init__(self, minx, maxx, miny, maxy, minz, maxz):
    self.minx = minx
    self.miny = miny
    self.minz = minz
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz
    self.on = False # default
    #self.add_bounds() #part1 only
    if minx > maxx or miny > maxy or minz > maxz:
      print ("BUG", self)
      exit(1)

  def add_bounds(self):
    if self.minx < -50:
      self.minx = -50
    if self.minx > 51:
      self.minx = 51

    if self.maxx < -50:
      self.maxx = -50
    if self.maxx > 51:
      self.maxx = 51

    if self.miny < -50:
      self.miny = -50
    if self.miny > 51:
      self.miny = 51

    if self.maxy < -50:
      self.maxy = -50
    if self.maxy > 51:
      self.maxy = 51

    if self.minz < -50:
      self.minz = -50
    if self.minz > 51:
      self.minz = 51

    if self.maxz < -50:
      self.maxz = -50
    if self.maxz > 51:
      self.maxz = 51

  def volume(self):
    return ((self.maxx - self.minx) * (self.maxy - self.miny) *
            (self.maxz - self.minz))


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

    if minx2 >= maxx1 or miny2 >= maxy1 or minz2 >= maxz1:
      return None

    if minx1 >= maxx2 or miny1 >= maxy2 or minz1 >= maxz2:
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

  def dimensions(self):
    return (self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz)


  def subtract(self, to_remove):
    """Subtract a cuboid from this one.
    Return all new cuboids created. Assume this one will be GCed afterwards.

    Args:
      to_remove: (Cuboid) a single cuboid to be subtracted from this one
    Return:
      [Cuboid, ...] A list of cuboids that remain when to_remove is gone.
    """
    newboids = []

    # Slice off and retain the left hand slab, if it exists.
    c, remainder = self.splitx(to_remove.minx)
    if c:
      newboids.append(c)
      #print("X1: Sliced off %s, leaving %s" % (c, remainder))
    #else:
      #print ("X1: Didn't get anything")
      
    # Slice off and retain the right hand slab of what's left, if it exists
    remainder, c = remainder.splitx(to_remove.maxx)
    if c:
      newboids.append(c)
      #print("X2: Sliced off %s, leaving %s" % (c, remainder))
    #else:
      #print ("X2: Didn't get anything")

    c, remainder = remainder.splity(to_remove.miny)
    if c:
      newboids.append(c)
      #print("Y1: Sliced off %s, leaving %s" % (c, remainder))
    #else:
      #print ("Y1: Didn't get anything")

    remainder, c = remainder.splity(to_remove.maxy)
    if c:
      newboids.append(c)
      #print("Y2: Sliced off %s, leaving %s" % (c, remainder))
    #else:
      #print ("Y2: Didn't get anything")

    c, remainder = remainder.splitz(to_remove.minz)
    if c:
      newboids.append(c)
      #print("Z1: Sliced off %s, leaving %s" % (c, remainder))
    #else:
      #print ("Z1: Didn't get anything")

    remainder, c = remainder.splitz(to_remove.maxz)
    if c:
      newboids.append(c)
      #print("Z2: Sliced off %s, leaving %s" % (c, remainder))
    #else:
      #print ("Z2: Didn't get anything")

    # TODO: the remainder should be all overlap
    # print ("The remainder is", remainder)
    return newboids


  def subtract_all(self, to_remove):
    """Remove a set of cuboids from this one, splitting this one into
       multiple pieces if needed. Return the pieces."""
    remaining = [self]
    next_remaining = []

    for c in to_remove:
      for r in remaining:
        overlap = c.overlap(r)
        if overlap:
          next_remaining.extend(r.subtract(overlap))
        else:
          next_remaining.append(r)
      remaining = list(next_remaining)

    return remaining


  def splitx(self, x):
    """Splits self along the x axis at x. Returns the two new cuboids (left,
    right). Does not modify self. GC happens elsewhere.
    The cuboid goes from min to max - 1 inclusive. A split can't put the same
    x in both cubes
    """
    if x <= self.minx:
      return None, self
    if x >= self.maxx:
      return self, None

    # So we're actually splitting.
    left = Cuboid(self.minx, x, self.miny, self.maxy, self.minz, self.maxz)
    right = Cuboid(x, self.maxx, self.miny, self.maxy, self.minz, self.maxz)
    return left, right

  def splity(self, y):
    """Splits self along the y axis at y. Returns the two new cuboids (top,
    bottom). Does not modify self. GC happens elsewhere.
    """
    if y <= self.miny:
      return None, self
    if y >= self.maxy:
      return self, None

    # So we're actually splitting.
    top = Cuboid(self.minx, self.maxx, self.miny, y, self.minz, self.maxz)
    bottom = Cuboid(self.minx, self.maxx, y, self.maxy, self.minz, self.maxz)
    return top, bottom

  def splitz(self, z):
    """Splits self along the z axis at z. Returns the two new cuboids (front,
    back). Does not modify self. GC happens elsewhere.
    """
    if z <= self.minz:
      return None, self
    if z >= self.maxz:
      return self, None

    # So we're actually splitting.
    front = Cuboid(self.minx, self.maxx, self.miny, self.maxy, self.minz, z)
    back = Cuboid(self.minx, self.maxx, self.miny, self.maxy, z, self.maxz)
    return front, back


  def __repr__(self):
    return "(x=%d/%d,y=%d/%d,z=%d/%d)" % (self.minx, self.maxx, self.miny,
                                          self.maxy, self.minz, self.maxz)

inputfile = "input22.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def testbig():
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

def testbiggest():
  lines="""on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""".split("\n")
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
    newboid = Cuboid(minx, maxx + 1, miny, maxy + 1, minz, maxz + 1)
    newboid.on = is_on
    cuboids.append(newboid)
  return cuboids



def test():
  lines = testsmall()
  cuboids = create(lines)
  assert (cuboids[0].volume() == 27)
  assert (cuboids[1].volume() == 27)

  newboid = cuboids[0].overlap(cuboids[1])
  assert(newboid.volume() == 8)

  remainder = cuboids[0].subtract(newboid)
  assert(sum([x.volume() for x in remainder]) == 19)

  newboid = cuboids[1].overlap(cuboids[0])
  assert(newboid.volume() == 8)

  newboid = cuboids[0].overlap(cuboids[2])
  assert(newboid.volume() == 8)

  newboid = cuboids[2].overlap(cuboids[0])
  assert(newboid.volume() == 8)

  newboid = cuboids[0].overlap(cuboids[3])
  assert(newboid.volume() == 1)

  assert (cuboids[3].volume() == 1)
  overlap = cuboids[3].overlap(cuboids[0])
  assert(overlap.volume() == 1)

  remainder = cuboids[0].subtract(overlap)
  assert(sum([x.volume() for x in remainder]) == 26)
  remainder = cuboids[3].subtract(overlap)

  newboid = cuboids[1].overlap(cuboids[3])
  assert(not newboid)

  newboid = cuboids[3].overlap(cuboids[1])
  assert(not newboid)

  newboid = cuboids[2].overlap(cuboids[3])
  assert(newboid.volume() == 1)
  newboid = cuboids[3].overlap(cuboids[2])
  assert(newboid.volume() == 1)

  firstboid = Cuboid(0, 3, 0, 3, 0, 3)
  left, right = firstboid.splitx(1)
  assert(left.dimensions() == (0, 1, 0, 3, 0, 3)), left.dimensions()
  assert(right.dimensions() == (1, 3, 0, 3, 0, 3)), right.dimensions()

  top, bottom = firstboid.splity(2)
  assert(bottom.dimensions() == (0, 3, 2, 3, 0, 3)), bottom.dimensions()
  assert(top.dimensions() == (0, 3, 0, 2, 0, 3)), top.dimensions()

  front, back = firstboid.splitz(3)
  assert(front.dimensions() == (0, 3, 0, 3, 0, 3)), front.dimensions()
  assert(not back), back

  print ("PASS")

#test()


on_cuboids = set()

#lines = testbig()
cuboids = create(lines)


for cuboid in cuboids:
  # if we're turning on one new cuboid containing a bunch of points
  # some of those points are already on but we'll deal with that later.
  if cuboid.on:
    on_cuboids.add(cuboid)
  else:
    # else if we're turning points off
    # compare it with every on_cuboid, find each overlap
    new_on_cuboids = set()
    while on_cuboids:
      on = on_cuboids.pop()
      overlap = cuboid.overlap(on)
      if overlap:
        # if there's an overlap, subtract the overlap from that on_cuboid
        # i.e., turn those points off
        # do that by creating up to six new on_cuboids and discarding the original
        replacementoids = on.subtract(overlap)
        new_on_cuboids.update(replacementoids)
      else:
        new_on_cuboids.add(on)
    on_cuboids = set(new_on_cuboids)

total = 0
done = []
all_on = deque(on_cuboids)

while all_on:
  c = all_on.popleft()
  found = False
  for d in done:
    overlap = d.overlap(c)
    if overlap:
      found = True
      newboids = c.subtract(d)
      all_on.extend(newboids)
      break
  if not found:
    done.append(c)

for d in done:
  print (d, d.volume())
  total += d.volume()

print (total)
