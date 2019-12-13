#!/usr/bin/python
# Advent of code day 12.

class Moon(object):
  def __init__(self, name, x, y, z):
    self.name = name
    self.x = x
    self.y = y
    self.z = z
    self.dx = 0
    self.dy = 0
    self.dz = 0
    self.xs = [x]
    self.ys = [y]
    self.zs = [z]

  def __repr__(self):
    return ("%s: pos=<x=%d, y=%d, z=%d>, vel=<x=%d, y=%d, z=%d>" %
      (self.name, self.x, self.y, self.z, self.dx, self.dy, self.dz))

  def apply(self, i):
    self.x += self.dx
    self.xs.append(self.x)
    self.y += self.dy
    self.ys.append(self.y)
    self.z += self.dz
    self.zs.append(self.z)

# Test input 1
moons = [
  Moon("A", -1, 0, 2),
  Moon("B", 2, -10, -7),
  Moon("C", 4, -8, 8),
  Moon("D", 3, 5, -1)
]

# Test input 2
moons = [
  Moon("A", -8, -10, 0),
  Moon("B", 5, 5, 10),
  Moon("C", 2, -7, 3),
  Moon("D", 9, -8, -3)
]

# Puzzle input
moons = [
  Moon("A", 4, 1, 1),
  Moon("B", 11, -18, -1),
  Moon("C", -2, -10, -4),
  Moon("D", -7, -2, 14)
]


edges = set()

for i in range(0, len(moons)):
  for j in range(i + 1, len(moons)):
    edges.add((moons[i], moons[j]))

n = 0
while True:
  for i, j in edges:
    if i.x < j.x:
      i.dx += 1
      j.dx -= 1
    elif i.x > j.x:
      j.dx += 1
      i.dx -= 1
    if i.y < j.y:
      i.dy += 1
      j.dy -= 1
    elif i.y > j.y:
      j.dy += 1
      i.dy -= 1
    if i.z < j.z:
      i.dz += 1
      j.dz -= 1
    elif i.z > j.z:
      j.dz += 1
      i.dz -= 1
  n += 1
  for moon in moons:
    moon.apply(n)
  if n == 1000000:
    break

  if n == 1000:
    energy = 0
    for moon in moons:
      potential = abs(moon.x) + abs(moon.y) + abs(moon.z)
      kinetic = abs(moon.dx) + abs(moon.dy) + abs(moon.dz)
      print moon.name, potential, kinetic
      x = potential * kinetic
      energy += x
    print "Part 1:", energy

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    """lowest common multiple"""
    return a * b / gcd(a, b)

# Find the index of a subsequence. From stack overflow. So lazy.
def index(subseq, seq):
    i, n, m = -1, len(seq), len(subseq)
    try:
        while True:
            i = seq.index(subseq[0], i + 1, n - m + 1)
            if subseq == seq[i:i + m]:
               return i
    except ValueError:
        return -1

solution = 1
for moon in moons:
  s1 = moon.xs
  s2 = moon.ys
  s3 = moon.zs

  xperiod = index(s1[0:1000], s1[1:]) +1
  yperiod = index(s2[0:1000], s2[1:]) +1 
  zperiod = index(s3[0:1000], s3[1:]) +1

  print "==>", xperiod, yperiod, zperiod
  lowest = lcm(xperiod, lcm(yperiod, zperiod))
  solution = lcm(solution, lowest)

print "Part 2:", solution

