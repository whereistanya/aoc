#!/usr/bin/env python
# Advent of code Day 2

with open("input2.txt", "r") as f:

  checksum1 = 0
  checksum2 = 0
  lines = f.readlines()
  for line in lines:
    values = sorted([int(x) for x in line.strip().split()])
    # Part 1
    checksum1 += int(values[len(values) -1]) - int(values[0])
    # Part 2
    for i in range(len(values)):
      value = values[i]
      for test in range(i + 1, len(values)):
        if values[test] % values[i] == 0:
          checksum2 += values[test] / values[i]
          break
  print checksum1
  print checksum2
