#!/usr/bin/env python

import sys

DEBUG = False

def joltage(count, line):
    readFrom = 0
    digits = [-1] * count
    i = 0 # index into digits

    for i in range(0, count):
      digits[i] = "9"
      while True:
        if int(digits[i]) < 0:
          print("Couldn't find digit ", i)
          print("Line was ", line)
          sys.exit(1)
        try:
          neededAfterThis = count - i - 1
          checkUntil = (len(line) - neededAfterThis)
          index = line[readFrom:checkUntil].index(digits[i]) + readFrom
        except ValueError:
          digits[i] = str(int(digits[i]) - 1)
          continue
        readFrom = index + 1
        break
    return int("".join(digits))


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

  for line in lines:
    if DEBUG:
      print(line)
    part1 += joltage(2, line)
    part2 += joltage(12, line)

  print("Part 1:", part1)
  print("Part 2:", part2)

main()
