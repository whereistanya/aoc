#!/usr/bin/env python3

import math
import re
import sys
import util.grid as g

test = True
test = False

if test:
  filename = "test23.txt"
else:
  filename = "input23.txt"


with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

field = g.Grid(lines)
field.printgrid()

def do_round(field, first_dir=0):
  elves = field.get_by_char("#")
  proposed_new_positions = {}

  for elf in elves:
    others = {}
    nabes = elf.neighbours_by_direction()
    for k, v in nabes.items():
      if v and v.value == "#":
        others[k] = v

    if not others:
      proposed_new_positions[elf] = (elf.x, elf.y)
      continue

    #print("neighbours", others)
    any_north = [d for d in others if d in ["northwest", "north", "northeast"]]
    any_south = [d for d in others if d in ["southwest", "south", "southeast"]]
    any_east = [d for d in others if d in ["northeast", "east", "southeast"]]
    any_west = [d for d in others if d in ["northwest", "west", "southwest"]]

    # n, s, w, e
    possible_positions = []
    new_pos = None
    if any_north:
      possible_positions.append(None)
    else:
      possible_positions.append(field.n_xy(elf))
    if any_south:
      possible_positions.append(None)
    else:
      possible_positions.append(field.s_xy(elf))
    if any_west:
      possible_positions.append(None)
    else:
      possible_positions.append(field.w_xy(elf))
    if any_east:
      possible_positions.append(None)
    else:
      possible_positions.append(field.e_xy(elf))

    for direction in range (first_dir, first_dir + 4):
      direction = direction % 4
      if possible_positions[direction]:
        new_pos = possible_positions[direction]
        break
    if not new_pos:
      # Stay still.
      new_pos = (elf.x, elf.y)
    proposed_new_positions[elf] = new_pos

  counts = {}
  for v in proposed_new_positions.values():
    try:
      counts[v] += 1
    except KeyError:
      counts[v] = 1

  field.grid.clear()
  moved = 0
  for elf, destination in proposed_new_positions.items():
    if counts[destination] == 1:
      if elf.x != destination[0] or elf.y != destination[1]:
        moved += 1
        elf.x = destination[0]
        elf.y = destination[1]
    field.addpoint(elf)

  assert(len(field.grid) == len(elves))
  #field.printgrid()
  return moved


i = 0
while True:
  #print("Starting round", i)
  moved = do_round(field, i)
  i += 1
  if moved == 0:
    break
  if i == 10:
    count = 0
    for y in range(field.miny, field.maxy):
      for x in range(field.minx, field.maxx):
        if (x, y) not in field.grid:
          count += 1
        elif field.getpoint(x, y).value != "#":
          count +=1
    print("Part 1: count was", count)

print("Part 2: Stopping after %d moves" % i)
