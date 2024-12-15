#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

gridlines = []
moveline = ""
movements = []
width = 0
for line in lines:
  if line.startswith("#"):
    gridline = ""
    for c in line:
      if c == "#":
        gridline += "##"
      if c == "O":
        gridline += "[]"
      if c == ".":
        gridline += ".."
      if c == "@":
        gridline += "@."
    gridlines.append(gridline)
  elif line.strip() == "":
    continue
  else:
    moveline += line.strip()

width = len(gridlines[0])
for c in moveline:
  movements.append(c)

grid = gridlib.Grid(gridlines)

grid.printnocolor()

dirs = {
  "^": grid.n,
  ">": grid.e,
  "v": grid.s,
  "<": grid.w
}

robot = grid.get_by_char("@")[0]

for move in movements:
  dirfunc = dirs[move]
  p = dirfunc(robot)
  if p.value == "#":
    continue
  if p.value == ".":
    robot.value = "."
    p.value = "@"
    robot = p
    continue
  needToMove = set([p])
  if p.value == "[":
    pair = grid.e(p)
  if p.value == "]":
    pair = grid.w(p)
  needToMove.add(pair)
  boxes = [] # list of sets to be moved in reverse order
  canPush = True

  while True:
    if not needToMove:
      break
    nextGroupToMove = set()
    beyond = set([n.value for n in needToMove])
    if "#" in beyond: # even one block stops everything
      canPush = False
      break

    for need in needToMove:
      if need.value not in ["[", "]"]:
        print("BUG: didn't expect a", need)
        grid.printnocolor()
        exit()
      nextpoint = dirfunc(need)
      if nextpoint in needToMove:
        continue
      if nextpoint.value == ".":
        continue
      nextGroupToMove.add(nextpoint)
      # Also add its pair if applicable
      if nextpoint.value == "[":
        alsoMove = grid.e(nextpoint)
        if alsoMove not in needToMove:
          nextGroupToMove.add(alsoMove)
      elif nextpoint.value == "]":
        alsoMove = grid.w(nextpoint)
        if alsoMove not in needToMove:
          nextGroupToMove.add(alsoMove)
    boxes.append(needToMove)
    needToMove = nextGroupToMove

  if canPush: # all in the same direction
    if move == "^" or move == "v": # vertical move
      for i in range(len(boxes) - 1, -1, -1):
        group = boxes[i]
        for box in group:
          dirfunc(box).value = box.value
          box.value = "."
    else: # horizontal move
      for i in range(len(boxes) - 1, -1, -1):
        group = boxes[i]
        if len(group) != 2:
          print("BUG: expected two, got", len(group))
          exit()
        xs = [dirfunc(box).x for box in group]
        ys = set([dirfunc(box).y for box in group])
        minx = min(xs)
        maxx = max(xs)
        if len(ys) > 1:
          print("BUG: expected horizontal, got", group)
          exit()
        y = ys.pop()
        for box in group:
          box.value = "."
        grid.getpoint_from_xy(minx, y).value = "["
        grid.getpoint_from_xy(maxx, y).value = "]"
    robot.value = "."
    p.value = "@"
    robot = p

grid.printnocolor()
boxes = grid.get_by_char("[")

part2 = 0
for box in boxes:
  pair = grid.e(box)
  part2 += box.x + 100 * box.y

print("Part 2:", part2)
