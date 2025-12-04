#!/usr/bin/env python3

import math
import re
import sys
import util.grid as g

test = False
test = True

if test:
  filename = "test22.txt"
else:
  filename = "input22.txt"

with open(filename, "r") as f:
  lines = [x[0:-1] for x in f.readlines()]


def parse_code(code):
  instrs = []
  s = ""
  for c in code:
    if c in ["L", "R"]:
      instrs.append((int(s), c))
      s = ""
    else:
      s += c
  if s != "":
    # spin in place at the end rather than handle a bare number specially
    instrs.extend([(int(s), "L"), (0, "L"), (0, "L"), (0, "L")])
  return instrs


code = lines[-1]
grid = g.Grid(lines[0:-1])

start = None
# Find the starting tile
for i in range(len(lines[0])):
  if lines[0][i] == ".":
    start = (i, 0)
    break
x, y = start

# Format the interesting features of the grid for easy retrieval.
rows, cols = grid.get_boundaries(["#", "."])

grid.grid[(x, y)].value = "O"
walls = [(p.x, p.y) for p in grid.get_by_char("#")]

row_walls = {}
col_walls = {}

for row in rows:
  row_walls[row] = []
for col in cols:
  col_walls[col] = []
for (_x, _y) in walls:
  row_walls[_y].append(_x)
  col_walls[_x].append(_y)

for row in rows:
  row_walls[row] = sorted(row_walls[row])
for col in cols:
  col_walls[col] = sorted(col_walls[col])


directions = ["e", "s", "w", "n"]
# initially facing right
direction = 0  # east

instrs = parse_code(code)
grid.printnocolor()





for instr in instrs:
  min_x = rows[y][0]
  max_x = rows[y][1] + 1
  min_y = cols[x][0]
  max_y = cols[x][1] + 1

  prev_x = x
  prev_y = y
  #print("The direction is now:", direction)
  #print("Beginning instruction:", instr)
  distance, turn = instr

  if direction == 0:
    #print("Moving %d east from %d, %d" % (distance, x, y))
    new_x = x + distance
    # first see if we run into anything before we loop
    for wall in row_walls[y]:
      if wall > x and wall <= new_x:
        new_x = wall - 1

    if new_x >= max_x: # we loop / move to another part of the cube
      if (min_x, y) in walls: # nowhere to loop to
        new_x = max_x - 1
      else:
        new_x = min_x + (new_x - max_x)
        for wall in row_walls[y]:
          if wall <= new_x:
            new_x = wall - 1
    move_to = (new_x, y)

  elif direction == 1: # south
    #print("Moving %d south from %d, %d" % (distance, x, y))
    new_y = y + distance
    for wall in col_walls[x]:
      if wall > y and wall <= new_y:
        new_y = wall - 1

    if new_y >= max_y: # we loop
      if (x, min_y) in walls:
        new_y = max_y - 1
      else:
        new_y = min_y + (new_y - max_y)
        for wall in col_walls[x]:
          if wall <= new_y:
            new_y = wall - 1
    move_to = (x, new_y)

  elif direction == 2: # west
    #print("Moving %d west from %d, %d" % (distance, x, y))
    new_x = x - distance
    for wall in row_walls[y]:
      if wall < x and wall >= new_x:
        new_x = wall + 1

    if new_x < min_x: # we loop
      if (max_x - 1, y) in walls:
        new_x = min_x
      else:
        new_x = max_x - (min_x - new_x)
        for wall in row_walls[y]:
          if wall >= new_x:
            new_x = wall + 1
    move_to = (new_x, y)

  elif direction == 3: # north
    #print("Moving %d north from %d, %d" % (distance, x, y))
    new_y = y - distance
    for wall in col_walls[x]:
      if wall < y and wall >= new_y:
        new_y = wall + 1
    if new_y < min_y: # we loop
      if (x, max_y - 1) in walls:
        new_y = min_y
      else:
        new_y = max_y - (min_y - new_y)
        for wall in col_walls[x]:
          if wall >= new_y:
            new_y = wall + 1
    move_to = (x, new_y)

  x, y = move_to
  if grid.grid[(x, y)].value not in [".", "o", "O"]:
    print("BUG: grid value is", grid.grid[(x, y)].value)
    exit(1)

  grid.grid[(x, y)].value = "o"
  if turn == "L":
    direction -= 1
  elif turn == "R":
    direction += 1
  else:
    print("BUG: turn was %s" % turn)
    exit(1)
  direction = direction % 4

#grid.printnocolor()

final_row = y + 1
final_col = x + 1

print("Part 1: password is", (1000 * final_row) + (4 * final_col) + direction)
