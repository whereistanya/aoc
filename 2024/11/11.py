#!/usr/bin/env python

from collections import defaultdict
import math

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  line = f.read().strip()

stones = defaultdict(int)
numbers = [int(x) for x in line.split()]
for number in numbers:
  stones[number] += 1

part1 = 0
part2 = 0

for i in range(75):
  nextStones = defaultdict(int)
  for stone, count in stones.items():
    if stone == 0:
      nextStones[1] += count
    else:
      digitCount = int(math.log10(stone)) + 1
      if digitCount % 2 == 0:
        # split into first n digits, second n digits
        power = pow(10, (digitCount / 2))
        first = int(stone / power)
        second = int(stone - (first * power))
        nextStones[first] += count
        nextStones[second] += count
      else:
        nextStones[stone * 2024] += count
  stones = nextStones
  stoneCount = 0
  for k, v in stones.items():
    stoneCount += v
  if i + 1 == 25:
    part1 = stoneCount
  elif i + 1 == 75:
    part2 = stoneCount

print("Part 1:", part1)
print("Part 2:", part2)
