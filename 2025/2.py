#!/usr/bin/env python

import sys

DEBUG = False

def main():
  filename = "input.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  with open(filename, "r") as f:
    line = f.read().strip()
  if DEBUG:
    print ("Using %s" % filename)
    print("Got input: %s" % line)

  part1 = 0
  part2 = 0

  ranges = line.split(",")
  for r in ranges:
    start, end = [int(x) for x in r.split("-")]
    invalids1 = set()
    invalids2 = set()

    # Are we brute forcing? We are!
    for number in range(start, end + 1):
      numbers = str(number)
      d = len(numbers)
      for i in range(1, d):
        if d % i != 0: # not possible to make a pattern of this many digits
          continue
        reps = int(d/i)
        pattern = int(numbers[0:i] * reps)
        if pattern >= start and pattern <= end:
          invalids2.add(pattern)
          if reps == 2:
            invalids1.add(pattern)

    part1 += sum(invalids1)
    part2 += sum(invalids2)

  print("Part 1:", part1)
  print("Part 2:", part2)

main()
