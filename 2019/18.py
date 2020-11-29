#!/usr/bin/python

import collections
import sys

class Key(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Grid(object):
  def __init__(self):
    self.path = set() # set of (x, y) tuples
    self.walls = set() # set of (x, y) tuples
    self.keys = {} # keyName: x, y
    self.doors = {} # doorName: x, y
    self.me = None # x, y of the character
    self.objects = {} # x, y : char. For drawing.
    self.height = 0
    self.width = 0
    self.distances = {} # (k1, k2): n  distance between keys
    self.blockers = {} # (k1, k2): [d1, d2]: which doors block visibility 
    self.shortest = 99999999999
    self.unblocked = {}
    self.robots = []

  def populate(self, lines):
    self.width = len(lines[0].strip())
    self.height = len(lines)
    for y in range(len(lines)):
      line = lines[y]
      for x in range(len(line.strip())):
        self.objects[(x, y)] = line[x]
        if line[x] == ".":
          self.path.add((x, y))
        if line[x] == "#":
          self.walls.add((x, y))
        elif line[x].islower():
          self.keys[line[x]] = (x, y)
        elif line[x].isupper():
          self.doors[line[x]] = (x, y)
        elif line[x] == "@":
          self.me = (x, y)  # part1
          self.objects[(x, y)] = str(len(self.robots)) # numbered robots
          self.robots.append((x, y)) # part2

    # TODO: Calculates everything twice. It's fine.
    self.populate_key_distance("@")
    self.populate_key_distance("0")
    self.populate_key_distance("1")
    self.populate_key_distance("2")
    self.populate_key_distance("3")
    for letter in self.keys:
      self.populate_key_distance(letter)

  def display(self):
    s = ""
    for y in range(self.height):
      s += "%d |" % y
      for x in range(self.width):
        if (x, y) in self.objects:
          s += self.objects[(x, y)]
      s += "\n"
    print(s.zfill(2))

  def neighbours(self, x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

  def populate_key_distance(self, key):
    # Find distances from this key to all other keys
    if key == "@":
      x, y = self.me  # part 1
    elif key in ["0", "1", "2", "3"]:
      x, y = self.robots[int(key)]
    else:
      x, y = self.keys[key]
    distance = 0
    to_check = collections.deque()
    doors_passed = []
    for neighbour in self.neighbours(x, y):
      if neighbour not in self.walls:
        to_check.append((neighbour[0], neighbour[1], 1, doors_passed))
    checked = set()
    while to_check:
      x, y, distance, doors_passed = to_check.popleft()
      doors = list(doors_passed)
      checked.add((x, y))
      if self.objects[(x, y)].isupper():
        doors.append(self.objects[(x, y)])
      if self.objects[(x, y)].islower():
        found = self.objects[(x, y)]
        if found != key:
          try:
            if distance < self.distances[(key, found)]:
              self.distances[(key, found)] = distance
          except KeyError:
              self.distances[(key, found)] = distance
          self.blockers[(key, found)] = doors
      for x1, y1 in self.neighbours(x, y):
        if (x1, y1) not in self.walls and (x1, y1) not in checked:
          to_check.append((x1, y1, distance + 1, doors))

  def visible_keys(self, start_key, existing_keys):
    """Return the new keys we can see from start_key.

    Args:
      start_key: (str) key or starting point to look from
      existing_keys: (str) list of keys we already have, joined in a string
                     to make it hashable
    """
    # What keys can we see from here without going through doors.
    # Takes existing_keys as a string so it's hashable and cacheable.
    if (start_key, existing_keys) in self.unblocked:
      return self.unblocked[(start_key, existing_keys)]
    visible_keys = []
    for key in self.keys:
      if key in existing_keys:
        continue
      visible = True
      try:
        blockers = self.blockers[(start_key, key)]
      except KeyError: # Not reachable from here
        continue
      for blocker in blockers:
        if blocker.lower() not in existing_keys:
          visible = False
          break
      if visible:
        visible_keys.append(key)
    self.unblocked[(start_key, existing_keys)] = visible_keys
    return visible_keys

    to_check = collections.deque()
    for d in self.neighbours(x, y):
      if d in self.path:
        to_check.append(d)
    checked = set()
    new_keys = []
    while to_check:
      x, y = to_check.popleft()
      checked.add((x, y))
      if self.objects[(x, y)].isupper():
        door = self.objects[(x, y)]
        #print "Door:", door
        if door.lower() not in existing_keys:
          # BLOCKED. Can't go here.
          continue
      if self.objects[(x, y)].islower():
        key = self.objects[(x, y)]
        if key not in existing_keys:
          new_keys.append(self.objects[(x, y)])
      for d in self.neighbours(x, y):
        if d not in self.walls and d not in checked:
          to_check.append(d)
    return new_keys

  def get_distance(self, key, locations):
    # return distance from any location, and the index of which location it was
    for i in range(0, 4):
      try:
        distance = self.distances[(locations[i], key)]
        return distance, i
      except KeyError:
        continue
    print("ERROR: Key %s didn't have a recorded distance from any of %s" % (key, locations))
    raise Exception

  def run_part2(self):
    to_check = collections.deque()
    shortest_distance = {}  # (sorted existing keys as str, last key): score
    initial_score = 0
    initial_locations = ["0", "1", "2", "3"]
    for i in range(0, 4):
      for key in self.visible_keys(initial_locations[i], ""):
        new_score, where = self.get_distance(key, initial_locations)
        new_score += initial_score
        new_locations = list(initial_locations)
        new_locations[where] = key
        to_check.append((key, new_score, new_locations))

    while len(to_check) > 0:
      existing_keys, existing_score, existing_locations = to_check.popleft()
      if len(existing_keys) == len(self.keys): # We have them all
        print("All keys!:", existing_keys, existing_score)
        if existing_score < self.shortest:
          self.shortest = existing_score

      new_keys = []
      for location in existing_locations:
        for new_key in self.visible_keys(location, existing_keys):
          # Find the distance from whichever robot can reach this.
          new_score, where = self.get_distance(new_key, existing_locations)
          s = "".join(sorted(list(existing_keys)))
          if (s, new_key) in shortest_distance: # We've been here before
            if shortest_distance[(s, new_key)] <= (existing_score + new_score):
              continue
          new_score += existing_score
          new_locations = list(existing_locations)
          new_locations[where] = new_key
          shortest_distance[(s, new_key)] = new_score
          s += new_key
          to_check.append((s, new_score, new_locations))

  def run_part1(self):
    to_check = collections.deque()
    shortest_distance = {}  # (sorted existing keys as str, last key): score

    initial_visible_keys = self.visible_keys("@", "")
    print(initial_visible_keys)
    for key in initial_visible_keys:
      to_check.append((key, self.distances[("@", key)]))
    while len(to_check) > 0:
      existing_keys, existing_score = to_check.popleft()
      last = existing_keys[-1]
      new_keys = self.visible_keys(last, existing_keys)
      if len(existing_keys) == len(self.keys):
        print("All keys:", existing_keys, existing_score)
        if existing_score < self.shortest:
          self.shortest = existing_score
      if new_keys:
        for new_key in new_keys:
          new_score = self.distances[(last, new_key)]
          x = sorted(list(existing_keys))
          s = "".join(x)
          if (s, new_key) in shortest_distance:
            if shortest_distance[(s, new_key)] <= (existing_score + new_score):
              continue
          shortest_distance[(s, new_key)] = (existing_score + new_score)
          s += new_key
          to_check.append((s, existing_score + new_score))


with open("input18b.txt", "r") as f:
  lines = f.readlines()

#with open("test18h.txt", "r") as f:
#  lines = f.readlines()

grid = Grid()
grid.populate(lines)
grid.display()
grid.run_part2()
print("Shortest was", grid.shortest)
