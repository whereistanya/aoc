#!/usr/bin/env python
# Advent of code Day 2.

import string
import sys

with open("day5input.txt", "r") as f:
  line = f.read().strip()

#line = "dabAcCaCBAcCcaDA"

def react(line):
  while True:
    start = line
    for i in string.ascii_lowercase:
      up = i.upper()
      #print i + up
      line = line.replace(i + up, "")
      line = line.replace(up + i, "")
      #print line
    if line == start:
      break
  return len(line)

shortest = 50001
should_remove = "unknown"

for i in string.ascii_lowercase:
  removed = line.replace(i, "")
  removed = removed.replace(i.upper(), "")
  count = react(removed)
  if count < shortest:
    shortest = count
    should_remove = i
  print i, react(removed)
print "Should remove %s, %d" % (should_remove, shortest)
