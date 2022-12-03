#!/usr/bin/env python3
# Advent of code Day 1.

with open("input1.txt", "r") as f:
  lines = f.readlines()

carries = {}

elf = 1
for line in lines:
  line = line.strip()
  if line == "":
    elf += 1
  else:
    try:
      carries[elf] += int(line)
    except KeyError:
      carries[elf] = int(line)

print ("Part 1", max(carries.values()))

v = sorted(carries.values(), reverse=True)
print ("Part 2", sum(v[0:3]))
