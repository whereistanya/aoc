#!/usr/bin/env python


target_x_min=20
target_x_max=30
target_y_min=-10
target_y_max=-5

# x=185..221, y=-122..-74
target_x_min=185
target_x_max=221
target_y_min=-122
target_y_max=-74


def in_target(x, y):
  if (x >= target_x_min and x <= target_x_max and
        y >= target_y_min and y <= target_y_max):
    return True
  return False

grid = {}

minxy = -10
maxxy = 30

for y in range(minxy, maxxy + 1):
  for x in range(minxy, maxxy + 1):
    if (x >= target_x_min and x <= target_x_max and
        y >= target_y_min and y <= target_y_max):
        grid[(x, y)] = "T"
    else:
      grid[(x, y)] = "."
grid[(0, 0)] = "S"


def fire(velx, vely):
  x = 0
  y = 0
  maxy = 0
  while True:
    x += velx
    y += vely
    if y < target_y_min:
      return False, 0
    if y > maxy:
      maxy = y
    if in_target(x, y):
      return True, maxy
    if velx < 0:
      velx += 1
    elif velx > 0:
      velx -= 1
    vely -= 1
    grid[(x, y)] = "#"

totalmaxy = 0
count = 0
for velx in range(0, 300):
  for vely in range(-300, 300):
    ok, maxy = fire(velx, vely)
    if ok:
      count += 1
      print velx, vely
      if maxy > totalmaxy:
        totalmaxy = maxy

print(totalmaxy, count)
