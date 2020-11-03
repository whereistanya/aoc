#!/usr/bin/env python
# Advent of code Day 56

import math

with open("input6.txt", "r") as f:
  lines = f.readlines()

  seen = set()

  values = lines[0].strip().split()
  values = ["0", "2", "7", "0"]
  steps = 0

  marker = ""
  cycle_counter = 0

  while True:
    svalues = ",".join(values)
    if svalues == marker:
      print ("Cycling again after %d cycles" % cycle_counter)
      break
    if svalues in seen:
      if marker == "":
        marker = svalues
        cycle_counter = 0
    seen.add(svalues)
    cycle_counter += 1

    # find the largest bank
    index = 0
    redistribute = 0

    for i in range(len(values)):
      value = values[i]
      if int(value) > redistribute:
        redistribute = int(value)
        index = i

    # redistribute
    values[index] = "0"
    while redistribute > 0:
      index = (index + 1) % len(values)
      values[index] = str(int(values[index]) + 1)  # abomination
      redistribute -= 1
    steps += 1

print ("Completed after %d steps" % steps)
