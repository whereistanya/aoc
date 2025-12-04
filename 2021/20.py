#!/usr/bin/env python3

import util.grid as grid

inputfile = "input20.txt"
inputfile = "input20.test"

with open(inputfile, "r") as f:
  algorithm = f.readline()
  print ("Algorithm: %s" % algorithm)
  print ("---------")
  _ = f.readline()
  lines = [x.strip() for x in f.readlines()]

def getindex(point, default="0"):
  neighbours = point.neighbours()

  s = ""
  for n in neighbours:
    if not n:
      s += default
      continue
    if n.value == ".":
      s += "0"
    elif n.value == "#":
      s += "1"
    else:
      print ("BUG:", n.value)
      exit(1)
  return int(s, 2)

def enhance(image, algorithm, default):
  new_values = {}
  outer_ring = []
  if default == "0":
    default_value = "."
  else:
    default_value = "#"

  to_check = []
  # (for full data) after one enhance, all pixels surrounded by off pixels turn
  # on. After the second one, all pixels surrounded by on pixels turn off.
  for x in range (image.minx - 1, image.maxx + 1):   # going wider for the outer layer
    for y in range (image.miny - 1, image.maxy + 1):
      to_check.append((x, y))

  for x, y in to_check:
    point = image.getpoint_from_xy(x, y, default_value)
    index = getindex(point, default)
    new_value = algorithm[index]
    new_values[(point.x, point.y)] = new_value
  for k, v in new_values.items():
    image.setvalue(k[0], k[1], v)

image = grid.Grid(lines)

for i in range(25):
  # The real input's algorithm has "00000000" => # and "11111111" => "."
  # so the "infinite" points will toggle on/off each turn.
  # For the test input, this needs to be 0, 0 instead.
  enhance(image, algorithm, "0")
  enhance(image, algorithm, "1")

image.printgrid()
print ([x.value for x in image.grid.values()].count("#"))

