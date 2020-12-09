#!/usr/bin/env python

inputfile = "input3.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

# Treating the string as an array, lovely.
"""
lines = [
  "..##.......",
  "#...#...#..",
  ".#....#..#.",
  "..#.#...#.#",
  ".#...##..#.",
  "..#.##.....",
  ".#.#.#....#",
  ".#........#",
  "#.##...#...",
  "#...##....#",
  ".#..#...#.#",
]
"""

slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]  # (y, x)!
counts = []

for slope in slopes:
  y = 0
  x = 0
  move_right = slope[0]
  move_down = slope[1]
  count = 0
  while y < len(lines):
    if lines[y][x] == "#":
      count += 1
    x += move_right
    x = x % len(lines[0])
    y += move_down

  print(count)
  counts.append(count)

product = 1
for count in counts:
  product *= count

print ("product:", product)
