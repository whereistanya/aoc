#!/usr/bin/env python3

import sys
import util.grid as gridlib

filename = "input.txt"
#filename = "test5"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

grid = gridlib.Grid(lines)

part1 = 0
part2 = 0

start = grid.get_by_char("S")[0]
print("Starting at", start)

def validval(direction, val):
  ok = {
    "north": ["|", "F", "7"],
    "east": ["-", "7", "J" ],
    "south": ["J", "|", "L"],
    "west": ["-", "F", "L" ],
  }
  if val in ok[direction]:
    return True
  return False

def validdir(val, direction):
  ok = {
    "S": ["north", "south", "east", "west"],
    "-": ["east", "west"],
    "|": ["north", "south"],
    "J": ["north", "west"],
    "F": ["south", "east"],
    "L": ["north", "east"],
    "7": ["south", "west"]
  }
  if direction in ok[val]:
    return True
  return False

# every pipe, including the one hidden under 'S', will have exactly two pipes pointing to it.
to_check = set([start])
start_neighbours = set()
for direction, neighbour in grid.neighbours_by_direction(start, diagonal=False).items():
  if neighbour is None:
    continue
  if validval(direction, neighbour.value):
    start_neighbours.add(direction)

if len(start_neighbours) != 2:
  print("Wrong number of start neighbours: %s" % start_neighbours)
  exit()

start_neighbours = sorted(start_neighbours)
dirs = (start_neighbours[0], start_neighbours[1])

start_secret_identity = {
  ( "north", "west" ): "J",
  ( "east", "north" ): "L",
  ( "south", "west" ): "7",
  ( "east", "south" ): "F",
}

startval = start_secret_identity[dirs]
start.value = startval

i = 0
in_loop = set([start])
while to_check:
  this_group = set(to_check)
  to_check.clear()
  i += 1
  for pos in this_group:
    in_loop.add(pos)
    neighbours = grid.neighbours_by_direction(pos, diagonal=False)
    for d, n in neighbours.items():
      if n is None:
        continue
      if n.value == ".":
        continue
      if not validdir(pos.value, d):
        continue
      if not validval(d, n.value):
        continue
      if n in in_loop:
        continue
      if n in to_check: # looped around! guess we're done
        part1 = i
        to_check.clear()
        in_loop.add(n)
        break
      to_check.add(n)
    if len(to_check) == 0: # none left, guess we're done
      part1 = i
      to_check.clear()
      break
    if len(to_check) > 2:
      print("Unexpected: from pos %s got %s" % (pos, to_check))
      exit()


print("Part 1:", part1)

def count_to_edge(point, grid, reverse=False):
  count = 0
  prev = ""
  if reverse:
    tiles = [grid.getpoint_from_xy(x, point.y) for x in range(0, point.x)]
  else:
    tiles = [grid.getpoint_from_xy(x, point.y) for x in range(point.x, grid.maxx)]
  for tile in tiles:
    x = tile.x
    if tile not in in_loop:
      continue
    if tile.value == "|":
      count += 1
      continue
    if tile.value == "S":
      print("Unexpected S value; should have been replaced earlier.")
      exit()
    if tile.value == "-":
      continue
    if tile.value in ["F", "L"]:
      prev = tile.value
      count += 1
    if tile.value == "7" and prev == "F":
      count += 1
      prev = 7
    if tile.value == "J" and prev == "L":
      count += 1
      prev = "J"
  return count

# count how many in_loop tiles are between this tile and any edge
# an odd number means it's in the loop; an even number means it's outside.
# only count crossing path segments, not individual tiles, e.g., .F--7. crosses
# one, not four

for point in grid.grid.values():
  if point in in_loop:
    continue
  count = count_to_edge(point, grid)
  if count % 2 == 1: # it's inside the loop
    point.value = "I"
    part2 += 1
  else:
    point.value = "O"

grid.printgrid()

print("Part 2:", part2)
