#!/usr/bin/env python3

import math
from collections import Counter

filename = "test17.txt"
filename = "input17.txt"


class Game(object):
  def __init__(self, jets):
    self.width = 7
    self.height = 4
    self.grid = set() # fallen rocks not current rock
    self.current = []
    self.next_rock = 0
    self.jets = jets
    self.next_jet = 0
    self.floor = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    self.grid.update(self.floor)
    self.tower_height = 0
    self.additions = []
    self.heights_at = {}

  def print(self):
    print("\n\n")

    for y in range(self.height, -1, -1):
      s = str(y).zfill(2)
      s += " "
      for x in range(-1, self.width + 1):
        if (x, y) in self.grid:
          s += "#"
        elif (x, y) in self.current:
          s += "@"
        elif (x, y) in self.floor:
          s += "-"
        elif x in [-1, 7]:
          s += "|"
        else:
          s += "."
      print(s)

  def can_move(self, pos):
    if any([p in self.grid for p in pos]):
      return False
    if any([x < 0 for (x, y) in pos]):
      return False
    if any([x > 6 for (x, y) in pos]):
      return False
    if any([y < 0 for (x, y) in pos]):
      return False
    return True

  def position_next_rock(self):
    rocks = [
      [(0, 0), (1, 0), (2, 0), (3, 0)], # horizontal
      [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], # cross
      [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], # ell
      [(0, 0), (0, 1), (0, 2), (0, 3)], # vertical
      [(0, 0), (1, 0), (0, 1), (1, 1)], # square
    ]
    rock = rocks[self.next_rock]
    adjx = 2
    adjy = self.height
    self.current = [(x + adjx, y + adjy) for (x, y) in rock]
    self.next_rock = (self.next_rock + 1) % 5

  def move_jets(self):
    c = self.jets[self.next_jet % len(self.jets)]
    if c == "<":
      #print("Push left")
      adjx = -1
    elif c == ">":
      #print("Push right")
      adjx = + 1
    else:
      print("BUG: unexpected input:", c)
      exit(1)
    self.next_jet += 1
    return adjx

  def drop_rock(self, i=0):
    self.position_next_rock()
    while True:
      adjx = self.move_jets()
      next_pos = [(x + adjx, y) for (x, y) in self.current]
      #if i == 763:
      #  print (next_pos)
      if self.can_move(next_pos):
        self.current = next_pos

      next_pos = [(x, y - 1) for (x, y) in self.current]
      if not self.can_move(next_pos):
        # stop moving
        self.grid.update(self.current)
        high_point = max([y for (x, y) in self.current])
        self.additions.append(high_point - self.tower_height)
        if high_point > self.tower_height:
          self.tower_height = high_point
        self.heights_at[i] = self.tower_height

        self.height = self.tower_height + 4
        break
      self.current = next_pos
      #self.print()


with open(filename, "r") as f:
  data = f.read().strip()

entry = 2 # two units away from the left wall
          # bottom edge is three units above the highest rock in the room


game = Game(data)
n = 10000
for i in range (n):
  game.drop_rock(i)
  #if ((i + 1) % 5 == 0):
  #  print(i + 1, game.tower_height)
print("Part 1", i + 1, game.tower_height)

# Find the cycle
cycle_length = -1
last_seen = -1
dists = []

# Get the least common number in the sequence and see if it repeats
# if not, try the second least common, etc.
most_common = Counter(game.additions).most_common()
for i in range(-1, -1 * (len(most_common)), -1):
  test, count = most_common[i]
  if count <= 1:
    continue
  for i in range (len(game.additions)):
    g = game.additions[i]
    if g == test:
      dists.append(i - last_seen)
      last_seen = i
  # Make sure all the distances between the appearance of the number have
  # the same value. Skip the first one because there's probably some time
  # before the repeat starts.
  if all(dists[1] == x for x in dists[1:]):
    cycle_length = dists[1]
    break  # because we found it.

if cycle_length == -1:
  print("BUG: never found a cycle length")
  exit(1)

# Now figure out when the cycle begins. There are a lot of non-repeated
# drops at the start before we start repeating.
repeats_at = -1
for i in range(0, cycle_length):
  if (game.additions[i: i + cycle_length] ==
      game.additions[i + cycle_length: i + cycle_length + cycle_length]):
    repeats_at = i
    break

if repeats_at == -1:
  print("BUG: never found a repeat")
  exit(1)

# Get the height change added each cycle.
cycle_added_height = (game.heights_at[(repeats_at + cycle_length)] -
                      game.heights_at[repeats_at])

# Double check it's right.
assert(game.heights_at[(repeats_at + cycle_length + cycle_length)] -
       game.heights_at[(repeats_at + cycle_length)] == cycle_added_height)

print ("Starts repeating after", repeats_at)
print("Repeats every %d drops" % cycle_length)
print("Every cycle we add", cycle_added_height)

n = 1000000000000
# Finally, figure out how many cycles we need to run, and how much extra
# to add (the offset) to get to exactly n cycles.
cycle_count = math.floor((n - repeats_at) / cycle_length)
offset = n - ((cycle_count * cycle_length) + repeats_at + 1)
print("Part 2:", game.heights_at[repeats_at + offset] +
                 (cycle_count * cycle_added_height))
