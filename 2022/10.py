#!/usr/bin/env python3
# Advent of code Day 10

#with open("test10.txt", "r") as f:
with open("input10.txt", "r") as f:
  lines = [x.strip().split() for x in f.readlines()]

regX = 1
c = 0
toFind = 20
signal = 0

for line in lines:
  c += 1 # whether it's an add or a noop
  if c == toFind:
    toFind += 40
    signal += (c * regX)
  instr = line[0]
  if instr == "addx":
    c += 1
    if c == toFind:
      toFind += 40
      signal += (c * regX)
    regX += int(line[1])

print("Part 1", signal)

pos = [" "] * 241
p = 0       # Position we're drawing now. p is always one less than the cycle
            # we're on (though cycle's only needed here when debugging.)
sprite = 1  # The number here defines the horizontal position in the middle, so
            # the sprite starts at [0, 1, 2]

for line in lines:
  if p % 40 in range (sprite - 1, sprite + 2):
    pos[p] = "#"
  else:
    pos[p] = "."
  instr = line[0]
  if instr == "addx":
    p += 1
    if p % 40 in range (sprite - 1, sprite + 2):
      pos[p] = "#"
    else:
      pos[p] = "."
    sprite += int(line[1])
  p += 1

print ("".join(pos[0:40]))
print ("".join(pos[40:80]))
print ("".join(pos[80:120]))
print ("".join(pos[120:160]))
print ("".join(pos[160:200]))
print ("".join(pos[200:240]))
