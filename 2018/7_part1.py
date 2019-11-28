#!/usr/bin/env python
# Advent of code Day 7.

import re
import sys

line_re = "Step (\w) must be finished before step (\w) can begin."

with open("day7input.txt", "r") as f:
  lines = f.readlines()

lines = [
  "Step C must be finished before step A can begin.",
  "Step C must be finished before step F can begin.",
  "Step A must be finished before step B can begin.",
  "Step A must be finished before step D can begin.",
  "Step B must be finished before step E can begin.",
  "Step D must be finished before step E can begin.",
  "Step F must be finished before step E can begin.",
]

depends = {}

for line in lines:
  letters = re.search(line_re, line).groups()
  if len(letters) != 2:
    print "Bad input"
    sys.exit(1)
  depender = letters[1]
  dependee = letters[0]

  try:
    depends[depender].append(dependee)
  except KeyError:
    depends[depender] = [dependee]

  if dependee not in depends:
    depends[dependee] = []

done = set()
ordered = ""

while depends:
# find what's available now
  available = []
  for k, values in depends.iteritems():
    if not values:
      available.append(k)
      continue
    if (all(v in done for v in values)):
      available.append(k)
      continue

  x = (sorted(available))[0]
  done.add(x)
  depends.pop(x)
  ordered += x

print ordered
