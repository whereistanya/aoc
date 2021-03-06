#!/usr/bin/env python
# Advent of code day 24.

def walk(moves):
  x = 0
  y = 0
# north is positive
  for move in moves:
    if move == "ne":
      x += 0.5
      y += 1
    elif move == "e":
      x += 1
    elif move == "se":
      x += 0.5
      y -= 1
    elif move == "sw":
      x -= 0.5
      y -= 1
    elif move == "w":
      x -= 1
    elif move == "nw":
      x -= 0.5
      y += 1
  return (x, y)

def getNeighbours(point):
  (x, y) = point
  return [(x + 0.5, y + 1), (x + 1, y), (x + 0.5, y - 1),
          (x - 0.5, y - 1), (x - 1, y), (x - 0.5, y + 1)]


# main()
with open("input24.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

# Parse
moveLists = []
for line in lines:
  i = 0
  moveList = []
  while (i < len(line)):
    if line[i:i + 2] in ["ne", "se", "nw", "sw"]:
      moveList.append(line[i:i + 2])
      i += 2
    else:
      moveList.append(line[i])
      i += 1
  moveLists.append(moveList)

# Part 1
blackTiles = set()

for moveList in moveLists:
  point = walk(moveList)
  try:
    blackTiles.remove(point)  # flip white
  except KeyError:
    blackTiles.add(point)     # flip black

print ("Part1: %d" % len(blackTiles))

# Part 2
for i in range(1, 101):
  blackNeighbourCount = {}  # How many black neighbours each tile has. (x, y): count
  for tile in blackTiles:
    for neighbour in getNeighbours(tile):
      try:
        blackNeighbourCount[neighbour] += 1
      except KeyError:
        blackNeighbourCount[neighbour] = 1

  nextBlackTiles = set()
  for tile, count in blackNeighbourCount.items():
    if tile in blackTiles and count in [1, 2]:
      nextBlackTiles.add(tile)  # stay black
    if tile not in blackTiles and count == 2:
      nextBlackTiles.add(tile)  # flip to black
  blackTiles = nextBlackTiles

print ("Part 2: %d" % len(blackTiles))
