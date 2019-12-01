#!/usr/bin/env python
# Advent of code Day 1.

import math

def fuel(mass):
  return math.floor(mass / 3.0) - 2

def everything(mass):
  x = fuel(mass)
  if x < 0:
    return 0
  return x + everything(x)

with open("input1.txt", "r") as f:

  assert fuel(12) == 2
  assert fuel(14) == 2
  assert fuel(1969) == 654
  assert fuel(100756) == 33583

  assert everything(14) == 2
  assert everything(1969) == 966
  assert everything(100756) == 50346

  total = 0
  lines = f.readlines()

  for line in lines:
    total += fuel(int(line.strip()))

  print("Total was %d" % total)

  total = 0
  for line in lines:
    total += everything(int(line.strip()))

  print("Total was %d" % total)
