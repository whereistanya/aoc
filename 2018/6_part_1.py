#!/usr/bin/env python
# Advent of code Day 6 part 1. Wildly overengineered.

with open("day6input.txt", "r") as f:
  lines = f.readlines()

######################################
# Part one
######################################

class Coord(object):
  """Coordinates from our list."""
  def __init__(self, xy):
    self.x, self.y = xy
    self.xy = xy
    self.locations = set()
    self.infinite = False

  def __repr__(self):
    return "Coord: %s, area: %d, infinite: %s" % (str(self.xy), len(self.locations),
                                                  self.infinite)

class Location(object):
  def __init__(self, xy, nearest_coord):
    self.x, self.y = xy
    self.xy = xy
    self.nearest_coord = nearest_coord  # Coord
    self.distance_from_coords = {}

  def __repr__(self):
    return str(self.xy)
    #return "Location: %s, nearest to: %s" % (self.xy, self.nearest_coord)

lines = [
  "1, 1",
  "1, 6",
  "8, 3",
  "3, 4",
  "5, 5",
  "8, 9"
]

coords = []  # [Coord, ...]

max_x = 0
max_y = 0

for line in lines:
  x, y = line.strip().split(", ")
  x = int(x)
  y = int(y)
  if x > max_x:
    max_x = x
  if y > max_y:
    max_y = y
  coords.append(Coord( (x, y)))

print(coords)
print(max_x, max_y)

locations = {}  # { (x, y): Location }
to_check = {}  # { (x, y): Location }

for coord in coords:
  # Initial locations are the listed coordinates
  locations[coord.xy] = Location(coord.xy, coord)
to_check = locations

seen = set()

steps = 0

while to_check:
  new_this_run = {} # {x, y): Location }
  steps += 1

  for location in list(to_check.values()):
    x, y = location.xy
    nearest_coord = location.nearest_coord
    location.distance_from_coords[nearest_coord] = steps

    north = (x, y - 1)
    south = (x, y + 1)
    west = (x - 1, y)
    east = (x + 1, y)

    for move in [north, south, east, west]:
      if move in new_this_run:
        move_location = new_this_run[move]
        if move_location.nearest_coord and move_location.nearest_coord != nearest_coord:
          move_location.nearest_coord.locations.remove(new_this_run[move])
          move_location.nearest_coord = None
        continue
      if move in seen:
        continue
      move_location = Location(move, nearest_coord)
      new_this_run[move] = move_location
      locations[move] = move_location
      nearest_coord.locations.add(move_location)

  to_check = {}
  for k in new_this_run:
    seen.add(k)
    if new_this_run[k].nearest_coord:
      # Should check for zero here; just being lazy with abs()
      if abs(new_this_run[k].x) <= max_x and abs(new_this_run[k].y) <= max_y:
        to_check[k] = new_this_run[k]
      else:
        new_this_run[k].nearest_coord.infinite = True


largest = 0
for coord in coords:
  if not coord.infinite:
    print(coord.xy, coord.locations, len(coord.locations))
    if len(coord.locations) > largest:
      largest = len(coord.locations)
print(largest)


for key in sorted(locations):
  print(location.xy, location.distance_from_coords)
