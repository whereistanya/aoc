#!/usr/bin/env python

import sys

DEBUG = False

def expand(line):
  i = 0
  newline = ""
  while i < len(line):
    nextchar = line[i]
    if nextchar == "(":
      close = line[i + 1:].index(")") + i + 1
      substr = line[i + 1: close]
      chars, repeats = [ int(x) for x in substr.split("x") ]
      torepeat = line[close + 1 : close + 1 + chars]
      repeated = (torepeat * repeats)
      newline += repeated
      i = close + 1 + chars
    else:
      newline += nextchar
      i += 1
  return newline


def expandv2(line):
  i = 0
  count = 0
  newline = ""
  while i < len(line):
    nextchar = line[i]
    if nextchar != "(":
      count += 1
      i += 1
      continue

    # opening a () section, recurse
    close = line[i + 1:].index(")") + i + 1
    substr = line[i + 1: close]
    chars, repeats = [ int(x) for x in substr.split("x") ]
    torepeat = line[close + 1 : close + 1 + chars]

    if "(" in torepeat:
      count += (repeats * expandv2(torepeat))
    else:
      count += repeats * chars
    i = close + len(torepeat) + 1

  return count



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

  assert(expand("A(1x5)BC") == "ABBBBBC")
  assert(expand("X(8x2)(3x3)ABCY") == "X(3x3)ABC(3x3)ABCY")

  part1 = len(expand(lines[0]))
  part2 = expandv2(lines[0])

  print("Part 1:", part1)
  print("Part 2:", part2)

main()
