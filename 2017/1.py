#!/usr/bin/env python
# Advent of code Day 1.

def add(digits, part):
  sum = 0
  l = len(digits)
  for i in range (0, l):
    if part == 1:
      compare = (i + 1) % l
    elif part == 2:
      compare = (i + (l / 2)) % l
    if digits[i] == digits[compare]:
      sum += int(digits[i])
  return sum

# Part 1
assert add([1,1,2,2], 1) == 3
assert add([9,1,2,1,2,1,2,9], 1) == 9

# Part 2
assert add([1,2,1,2], 2) == 6
assert add([1,2,1,3,1,4,1,5], 2) == 4

with open("input1.txt", "r") as f:
  digits = list(f.read().strip())
  print add(digits, 1)
  print add(digits, 2)


