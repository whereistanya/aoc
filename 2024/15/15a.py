#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

filename = "input.txt"
#filename = "test1"
#filename = "test2"


with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

gridlines = []
moveline = ""
movements = []
for line in lines:
  if line.startswith("#"):
    gridlines.append(line)
  elif line.strip() == "":
    continue
  else:
    moveline += line.strip()

for c in moveline:
  movements.append(c)

grid = gridlib.Grid(gridlines)

dirs = {
  "^": grid.n,
  ">": grid.e,
  "v": grid.s,
  "<": grid.w
}

robot = grid.get_by_char("@")[0]

for move in movements:
  #grid.printgrid()
  dirfunc = dirs[move]
  p = dirfunc(robot)
  if p.value == "#":
    continue
  if p.value == ".":
    robot.value = "."
    p.value = "@"
    robot = p
    continue
  if p.value == "O":
    boxes = [p]
    canPush = True
    nextpoint = dirfunc(p)
    while True:
      beyond = nextpoint.value
      if beyond == "#":
        canPush = False
        break
      if beyond == ".":
        break
      if beyond == "O": # there's another box, go further
        boxes.append(nextpoint)
        nextpoint = dirfunc(nextpoint)

  if canPush:
    dirfunc(boxes[-1]).value = boxes[-1].value
    for i in range(len(boxes) - 1, 0, -1):
      boxes[i].value = boxes[i - 1].value
    robot.value = "."
    p.value = "@"
    robot = p

boxes = grid.get_by_char("O")
part1 = 0

for box in boxes:
  part1 += box.x + 100 * box.y

print("Part 1:", part1)
