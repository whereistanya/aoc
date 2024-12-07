#!/usr/bin/env python

filename = "input.txt"
#filename = "test1"

def equate(numbers, total, part2=False):
  toTry = set([numbers[0]])
  toTryNext = set()

  for n in numbers[1:]:
    toTryNext = set()
    for start in toTry:
      toTryNext.add(start + n)
      toTryNext.add(start * n)

      if part2:
        concatted = int(str(start) + str(n))
        toTryNext.add(concatted)
    toTry = set(toTryNext)
  if total in toTry:
    return True
  return False



with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

part1 = 0
part2 = 0
for line in lines:
  total, numstr = line.split(":")
  numbers = [int(x) for x in numstr.split()]
  total = int(total)

  ok = equate(numbers, total)
  if ok:
    part1 += total

  ok = equate(numbers, total, part2=True)
  if ok:
    part2 += total

print("Part 1:", part1)
print()
print("Part 2:", part2)
