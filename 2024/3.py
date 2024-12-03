#!/usr/bin/env python

filename = "input.txt"
#filename = "test2"


with open(filename, "r") as f:
  line = f.read()

part1 = 0
part2 = 0

i = 0
doTheThing = True

while i < len(line):
  # don't()
  if line[i:].startswith("don't()"):
    doTheThing = False
    i += 7
    continue

  # do()
  if line[i:].startswith("do()"):
    doTheThing = True
    i += 4
    continue

  # valid mul()
  if line[i:].startswith("mul("):
    close = line[i:].index(")")
    nums = line[i + 4 : i + close].split(",")
    if len(nums) == 2 and nums[0].isnumeric() and nums[1].isnumeric():
      mul = int(nums[0]) * int(nums[1])
      part1 += mul
      if doTheThing:
        part2 += mul
      i += close
      continue


  # invalid mul()
    i += 4
    continue

  # didn't match anything
  i += 1

print("Part 1:", part1)
print("Part 2:", part2)
