#!/usr/bin/env python
# Advent of code Day 5.

with open("input5.txt", "r") as f:
  lines = [int(x.strip()) for x in f.readlines()]

  #lines = [0, 3, 0, 1, -3]
  steps = 0

  i = 0
  while True:
    try:
      instruction = lines[i]
      steps += 1
    except IndexError:
      break
    # part 1
    offset = 1
    # part 2
    if instruction >= 3:
      offset = -1
    lines[i] += offset
    i += instruction

print(steps)
