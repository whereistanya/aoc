#!/usr/bin/env python

import sys

DEBUG = False

class Range(object):
  def __init__(self, start, end):
    self.valid = True
    self.start = start
    self.end = end

  def in_range(self, val):
    if val >= self.start and val <= self.end:
      return True
    return False

  def size(self):
    return self.end - self.start + 1

  def __repr__(self):
    return "Range(%d-%d=%d)" % (self.start, self.end, self.size())

def main():
  filename = "input.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  with open(filename, "r") as f:
    lines = [x.strip() for x in f.readlines()]
  if DEBUG:
    print ("Using %s" % filename)
    print("Got input: %s" % lines)

  part1 = 0
  part2 = 0

  ranges = []
  ingredients = []
  for line in lines:
    if "-" in line:
      s, e = line.split("-")
      ranges.append(Range(int(s), int(e)))
    elif line == "":
      continue
    else:
      ingredients.append(int(line))

  for ingredient in ingredients:
    for r in ranges:
      if r.in_range(ingredient):
        part1 += 1
        break


  overlaps = True
  while overlaps:
    overlaps = False
    for r1 in ranges:
      if not r1.valid:
        continue
      for r2 in ranges:
        if not r2.valid:
          continue
        if r1 == r2:
          continue
        if r1.in_range(r2.start):
          if r1.in_range(r2.end): # this range is entirely enclosed
            r2.valid = False
            if DEBUG:
              print(r2, "entirely enclosed by", r1)
            overlaps = True
            break
          else: # start is in range, but end isn't
            if DEBUG:
              print(r2, "overlaps with", r1)
            r2.start = r1.end + 1
            overlaps = True
        else:
          if r1.in_range(r2.end): # end is in range but start isn't
            if DEBUG:
              print(r2, "overlaps with", r1)
            r2.end = r1.start - 1
            overlaps = True

  for r in ranges:
    if not r.valid:
      continue
    part2 += r.size()


  print("Part 1:", part1)
  print("Part 2:", part2)

main()
