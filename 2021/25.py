#!/usr/bin/env python

import util.grid as grid

inputfile = "input25.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test1():
  lines = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".split("\n")
  return lines

def test2():
  lines = """...>>>>>...""".split("\n")
  return lines

def test3 ():
  lines = """..........
.>v....v..
.......>..
..........""".split("\n")
  return lines

def test4():
  lines = """...>...
.......
......>
v.....>
......>
.......
..vvv..""".split("\n")
  return lines




def step(space):
  moved = False
  gridcopy = dict(space.grid)
  for xy in space.grid:
    sc = space.grid[xy]
    # Move East
    if sc.value == ">":
      newx = (sc.x + 1) % space.maxx
      right = space.grid[(newx, sc.y)].value # looking at original
      if right == ".":
        moved = True
        gridcopy[(sc.x, sc.y)] = grid.Point(sc.x, sc.y, ".", space)
        sc.x = newx
        gridcopy[(newx, sc.y)] = sc
  space.grid = gridcopy
  gridcopy = dict(space.grid)
  for xy in space.grid:
    sc = space.grid[xy]
    # Move South
    if sc.value == "v":
      newy = (sc.y + 1) % space.maxy
      down = space.grid[(sc.x, newy)].value # looking at original
      if down == ".":
        moved = True
        gridcopy[(sc.x, sc.y)] = grid.Point(sc.x, sc.y, ".", space)
        sc.y = newy
        gridcopy[(sc.x, newy)] = sc
  space.grid = gridcopy
  return moved


#lines = test1()
space = grid.Grid(lines)
i = 0
while True:
  moved = step(space)
  i += 1
  if not moved:
    break

space.printgrid()
print(i)
