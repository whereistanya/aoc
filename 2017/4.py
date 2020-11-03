#!/usr/bin/env python
# Advent of code Day 4.

with open("input4.txt", "r") as f:
  lines = f.readlines()
  count = 0

# Part 1
for line in lines:
  values = line.strip().split()
  words = set()
  valid = True
  for value in values:
    if value in words:
      valid = False
      break
    words.add(value)
  if valid:
    count += 1

print count

# Part 2
count = 0
for line in lines:
  values = line.strip().split()
  words = set()
  valid = True
  for value in values:
    svalue = str(sorted(value))
    if svalue in words:
      valid = False
      break
    words.add(svalue)
  if valid:
    count += 1


print count
