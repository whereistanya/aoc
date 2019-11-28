#!/usr/bin/env python
# Advent of code Day 20.


class Room(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.neighbours = {} # str: Room

  def __repr__(self):
    return "(%d, %d: %d doors)" % (self.x, self.y, len(self.neighbours))

class Grid(object):
  def __init__(self):
    self.rooms = {}  # (x,y): Room
    self.min_x = 99999999999999999
    self.max_x = 0
    self.min_y = 99999999999999999
    self.max_y = 0

  def neighbour(self, x, y, direction):
    if direction == "N":
      return x, y - 1
    if direction == "S":
      return x, y + 1
    if direction == "E":
      return x + 1, y
    if direction == "W":
      return x - 1, y
    print "Error: bad direction", direction
    return None, None

  def build_room(self, x, y):
    if x > self.max_x: self.max_x = x
    if x < self.min_x: self.min_x = x
    if y > self.max_y: self.max_y = y
    if y < self.min_y: self.min_y = y
    return Room(x, y)

  def walk(self, regex, room):
    consumed = 0
    # breaks if first char isn't ^

    opposites = {
      "S": "N", "N": "S",
      "E": "W", "W": "E",
    }

    i = 0
    while True:
      consumed += 1
      c = regex[i]
      if c == "^":
        room = Room(0, 0)
        self.rooms[(0, 0)] = room
        i += 1
        continue
      if c in ["N", "S", "E", "W"]:
        next_x, next_y = self.neighbour(room.x, room.y, c)
        if (next_x, next_y) in self.rooms:
          next_room = self.rooms[(next_x, next_y)]
        else:
          next_room = self.build_room(next_x, next_y)
          self.rooms[(next_x, next_y)] = next_room
        room.neighbours[c] = next_room
        next_room.neighbours[opposites[c]] = room
        room = next_room
        i += 1
        continue
      if c == "(":
        while True:
          # we're branching
          child_consumed = self.walk(regex[i + 1:], room)
          consumed += child_consumed
          i += 1
          # will return to the same point; jump forward to the next | or )
          try:
          #  while regex[i] not in ["|", ")"]:
            for x in range(0, child_consumed - 1):
              i += 1
          except IndexError:
            return consumed
          if regex[i] == ")":
            break
        i += 1
        continue
      if c in ["|", ")", "$"]:
        return consumed

  def draw(self):
    print "x: %d to %d. y: %d to %d" % (self.min_x, self.max_x, self.min_y, self.max_y)
    # Each room is drawn in two passes: north wall, east/west walls.
    # The south wall comes from the room below.
    for y in range(self.min_y, self.max_y + 1):
      s1 = ""
      s2 = ""
      found = []
      for x in range(self.min_x, self.max_x + 1):
        try:
          room = self.rooms[(x, y)]
          found.append(room)
          if "N" in room.neighbours:
            s1 += "#-"
          else:
            s1 += "##"

          if "W" in room.neighbours:
            s2 += "|."
          else:
            s2 += "#."
        except KeyError:
          print "No %d,%d" % (x, y)
          s1 += "??"
          s2 += "??"
      # Fencepost
      s1 += "#  "
      s1 += str(found)
      try:
        room = self.rooms[(self.max_x, y)]
        if "E" in room.neighbours:
          s2 += "|"
        else:
          s2 += "#"
      except KeyError:
        s2 += "?"
      print s1
      print s2
    # Last line
    s3 = ""
    for x in range(self.min_x, self.max_x + 1):
      try:
        room = self.rooms[(x, self.max_y)]
        if "S" in room.neighbours:
          s3 += "#-"
        else:
          s3 += "##"
      except KeyError:
        s3 += "??"
    s3 += "#"
    print s3

  def bfs(self):
    initial = self.rooms[(0, 0)]
    to_check = [x for x in initial.neighbours.values()]
    checked = set()
    i = 0
    far_rooms = 0
    while to_check:
      this_round = list(to_check)
      to_check = []
      i += 1
      if i >= 1000:
        far_rooms += len(this_round)
      for room in this_round:
        checked.add(room)
        for neighbour in room.neighbours.values():
          if neighbour not in checked:
            to_check.append(neighbour)
    return i, far_rooms


regex = "^WNE$"
regex = "^ENWWW(NEEE|SSE(EE|N))"
regex = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
regex = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
regex = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"

with open("day20input.txt", "r") as f:
  regex = f.readlines()[0]
grid = Grid()
grid.walk(regex, None)
#grid.draw()  # only for small ones!

print grid.bfs()  # part1, part2
