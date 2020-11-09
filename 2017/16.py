#!/usr/bin/env python
# Advent of code Day 16.


class Dance(object):
  def __init__(self, programs):
    self.front = 0
    self.programs = programs
    self.length = len(programs)
    self.positions = {}
    for i in range(len(programs)):
      self.positions[programs[i]] = i
    self.start = ''.join(self.programs)

  def spin(self, count):
    # X programs move from the end to the front
    # we adtually just move what we consider the front to be
    self.front = (self.front + (self.length - count)) % self.length

  def get(self, position):
    # gets the program at a position, adjusted for where the front is
    return self.programs[(position + self.front) % self.length]

  def put(self, position, value):
    self.programs[(position + self.front) % self.length] = value
    self.positions[value] = (position + self.front) % self.length

  def find(self, value):
    return self.positions[value] - self.front

  def xchange(self, posa, posb):
     # the programs at positions A and B swap places
    tmp = self.get(posa)
    self.put(posa, self.get(posb))
    self.put(posb, tmp)

  def partner(self, a, b):
    # the programs named A and B swap places
    posa = self.find(a)
    posb = self.find(b)
    self.xchange(posa, posb)

  def display(self):
    # Creates a new list, so use sparingly.
    return [self.programs[(i + self.front) % self.length] for i in range(self.length)]

with open("input16.txt", "r") as f:
  moves = f.read().strip().split(",")

programs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']


"""
dance.display()
dance.partner('b', 'd')
dance.display()
dance.partner('c', 'd')
dance.display()
dance.spin(3)
dance.display()
dance.xchange(3,4)
dance.display()

programs = ['a', 'b', 'c', 'd', 'e']
moves = [
  's1',   # a spin of size 1: eabcd.
  'x3/4', # swapping the last two programs: eabdc.
  'pe/b',
]
"""


dance = Dance(programs)
# Cycle repeats every 48 times
# back to start at 47, 95, 143, 191, ..., 9999983
# so running 16 times should be the same as running 1 billion times.
times = 16

for time in range(times):
  for move in moves:
    if move.startswith("s"):
      count = int(move[1:])
      dance.spin(count)
    elif move.startswith("x"):
      a, b = [int(x) for x in move[1:].split("/")]
      dance.xchange(a, b)
    elif move.startswith("p"):
      a, b = move[1:].split("/")
      dance.partner(a, b)
    else:
      print "unexpected:", move
      exit()
  s = "".join(dance.display())
  if s == dance.start:
    print "Back to start after", time, "times"
    exit()

print "After", times, "times:", s

