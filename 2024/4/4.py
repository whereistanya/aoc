#!/usr/bin/env python


import re
import sys
sys.path.append("../../")
import util.grid
filename = "input.txt"
#filename = "test1"


with open(filename, "r") as f:
  lines= [x.strip() for x in f.readlines()]


# Part 1

width = len(lines[0])
height = len(lines)

print ("horizontals")
allLines = []
for line in lines:
  allLines.append(line)
  print(line)
  allLines.append(line[::-1])

print ("verticals")
for i in range(width):
  vertical = ""
  for j in range(height):
    vertical += lines[j][i]
  print(vertical)
  allLines.append(vertical)
  allLines.append(vertical[::-1])


print("diagonals down/right along side (y=0)")
for y in range(height):
  x = 0 # left side
  diag = ""
  while True:
    try:
      diag += lines[y][x]
    except IndexError:
      allLines.append(diag)
      allLines.append(diag[::-1])
      print(diag)
      print(diag[::-1])
      break
    x += 1
    y += 1

print("diagonals down/right along top x=0")
for x in range(1, width):  # 0 caught by previous
  y = 0 # top
  diag = ""
  while True:
    try:
      diag += lines[y][x]
    except IndexError:
      allLines.append(diag)
      allLines.append(diag[::-1])
      print(diag)
      print(diag[::-1])
      break
    x += 1
    y += 1


print("diagonals down/left along side (y=max)")
for y in range(height):
  x = width -1 # right side
  diag = ""
  while True:
    if y < 0:
      allLines.append(diag)
      allLines.append(diag[::-1])
      print(diag)
      print(diag[::-1])
      break
    try:
      diag += lines[y][x]
    except IndexError:
      allLines.append(diag)
      allLines.append(diag[::-1])
      print(diag)
      print(diag[::-1])
      break
    y += 1
    x -= 1

print("diagonals down/left along top x=max")
for x in range(width - 2, 0, -1):  # 0 caught by previous
  y = 0 # top
  diag = ""
  while True:
    if x < 0:
      allLines.append(diag)
      allLines.append(diag[::-1])
      print(diag)
      print(diag[::-1])
      break
    try:
      diag += lines[y][x]
    except IndexError:
      allLines.append(diag)
      allLines.append(diag[::-1])
      print(diag)
      print(diag[::-1])
      break
    x -= 1
    y += 1


print(allLines)

count = 0
for line in allLines:
  count += line.count("XMAS")

print(count)


part1 = 0
part2 = 0

# Part 2

allLines = []

for y in range(1, height - 1):
  for x in range(1, width - 1):
    if lines[y][x] != 'A':
      continue
    pattern1 = lines[y - 1][x - 1] + 'A' + lines[y + 1][x + 1]
    pattern2 = lines[y - 1][x + 1] + 'A' + lines[y + 1][x - 1]
    print ("*", pattern1, pattern2)

    if pattern1 in ["MAS", "SAM"] and pattern2 in ["MAS", "SAM"]:
      allLines.append(pattern1)

print (len(allLines))

print("Part 1:", part1)
print("Part 2:", part2)

