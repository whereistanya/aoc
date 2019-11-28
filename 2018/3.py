#!/usr/bin/env python
# Advent of code Day 3.

import re
import sys

line_re = "#(\d+) @ (\d+),(\d+): (\d+)x(\d+)"

class Claim(object):
  def __init__(self, claim_id, x, y, width, height):
    """Dimensions of rectangle. x, y is top left corner."""
    self.id = claim_id
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.inches = self.covered_inches()

  def __repr__(self):
    return "%d: %d,%d %dx%d" % (self.id, self.x, self.y, self.width, self.height)

  def covered_inches(self):
    """Return a set of x,y co-ords of inches covered by this rectangle.
    """
    # from x to x+width
    # from y to y+height
    inches = set()
    for i  in range(self.x, self.x + self.width):
      for j in range (self.y, self.y + self.height):
        inches.add((i, j))
    return inches

def parse_line(line):
  groups = re.search(line_re, line).groups()
  if len(groups) != 5:
    print("Bad input [%s] matched [%s]" % (line, groups))
    sys.exit(1)
  return Claim(int(groups[0]), int(groups[1]), int(groups[2]), int(groups[3]),
               int(groups[4]))


with open("day3input.txt", "r") as f:
  lines = f.readlines()

claims = []
covered = set()
overlaps = set()

#lines = [
#  "#1 @ 1,3: 4x4",
#  "#2 @ 3,1: 4x4",
#  "#3 @ 5,5: 2x2",
# ]

for line in lines:
  claim = parse_line(line)
  claims.append(claim)
  inches = claim.inches
  for inch in inches:
    if inch in covered:
      overlaps.add(inch)
    covered.add(inch)

print "%d inches are within two or more claims." % len(overlaps)

# Only one claim fits in covered - overlaps
non_overlapping = covered - overlaps

for claim in claims:
  if claim.inches.issubset(non_overlapping):
    print claim
