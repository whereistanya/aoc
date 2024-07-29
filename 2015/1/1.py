#!/usr/bin/env python3
# Code by Ms 11!

floor = 0
position = 0
with open("input.txt", "r") as f:
  lines = f.readlines()
line = lines[0]
print (line)
for c in line:
  if c == "(":
    floor += 1
  else:
    floor -= 1
  position += 1
  if floor == -1:
    print (position)
    break

print (floor)
