#!/usr/bin/env python

input10 = "183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88".split(",")
lengths = [int(x) for x in input10]
n = 256

lengths = [3, 4, 1, 5]
n = 5

values = [x for x in range(0, n)]
skip_size = 0
index = 0

for length in lengths:
  substr = values[index: index + length]
  if index + length > len(values):
    substr += values[0: (index + length) - len(values)]
  substr.reverse()

  for i in range(len(substr)):
    values[(index + i) % len(values)] = substr[i]
  index += (length + skip_size)
  index = index % len(values)
  skip_size += 1

print "Part 1:", values[0] * values[1]
