#!/usr/bin/env python

import sys
import util.grid as gridlib

DEBUG = True

def main():
  filename = "input.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  with open(filename, "r") as f:
    instructions = [x.strip() for x in f.readlines()]
  if DEBUG:
    print ("Using %s" % filename)
    print("Got input: %s" % instructions)

  part1 = 0
  part2 = 0

  width = 50
  height = 6

  #width = 7
  #height = 3

  line = width * "."
  lines = height * [line]
  grid = gridlib.Grid(lines)
  grid.printgrid()

  for ins in instructions:
    if ins.startswith("rect"):
      w, h = [int(x) for x in ins.split(" ")[1].split("x")]
      for x in range(0, w):
        for y in range(0, h):
          point = grid.getpoint_from_xy(x, y)
          point.value = "#"
      grid.printgrid(summary=False)

    elif ins.startswith("rotate column"):
      # e.g., rotate column x=1 by 1
      col, val = [int(x) for x in ins.split("=")[1].split(" by ")]
      points = grid.get_col(col)
      current = [x.value for x in points]
      for i in range(len(points)):
        points[i].value = current[(i - val) % len(points)]
      grid.printgrid(summary=False)

    elif ins.startswith("rotate row"):
      # rotate row y=1 by 1
      row, val = [int(x) for x in ins.split("=")[1].split(" by ")]
      points = grid.get_row(row)
      current = [x.value for x in points]
      for i in range(len(points)):
        points[i].value = current[(i - val) % len(points)]
      grid.printgrid(summary=False)

    else:
      print("Unexpected instruction: ", ins)
      sys.exit(1)

  points = grid.get_by_char("#")
  print(len(points))

  print("Part 1:", part1)
  print("Part 2:", part2)

main()
