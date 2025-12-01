#!/usr/bin/env python

import sys

DEBUG = False

def main():
  filename = "input.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  with open(filename, "r") as f:
    lines = [x.strip() for x in f.readlines()]
  if DEBUG:
    print ("Using %s" % filename)

  part1 = 0
  part2 = 0
  dial = 50

  for step in lines:
    direction = step[0]
    if direction not in ["R", "L"]:
      print("Parse error: weird direction")
      sys.exit(1)

    number = int(step[1:])

    rotations = int(number / 100)
    remain = number % 100
    assert((rotations * 100) + remain == number), "Error: universe does not work like you think"

    if direction == "L":
      remain *= -1

    dial = (dial + remain) % 100
    if DEBUG:
      print("The dial is rotated %s: %d rotations and then %d, stopping at %d" % (step, rotations, remain, dial))

    part2 += rotations # went around at least this many times
    if dial == 0:
      part1 += 1 # at zero
      part2 += 1 # touched zero
    else: # not at zero, but did it pass zero to get here?
      if (dial - remain) < 0 or (dial - remain) > 100:
        part2 += 1


  print("Part 1:", part1)
  print("Part 2:", part2)

main()
