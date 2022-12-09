#!/usr/bin/env python3
# Advent of code Day 8

#with open("test8.txt", "r") as f:
with open("input8.txt", "r") as f:
  lines = [[int(x) for x in line]
            for line in [x.strip() for x in f.readlines()]]

# Yeah, globals
maxx = len(lines[0])
maxy = len(lines)

def look_part_a(line, heights):
  """Start at the first point in the line, see how far you can see.

    A tree is visible if all the trees between here and there (including
    the first one) are shorter than it.
  """
  n = 0
  can_see = []
  min_visible = heights[line[0]]
  while (n + 1) < len(line):
    tree = line[(n + 1)]
    if heights[tree] > min_visible:
      min_visible = heights[tree]
      can_see.append(tree)
    n += 1
  return can_see

def look_part_b(line, heights):
  """Start at the first point in the line, see how far you can see.

    A tree is visible if it and all the trees between here and there
    (excluding the first one) are shorter than the first one.
  """
  n = 0
  can_see = []
  max_visible = heights[line[0]]
  while (n + 1) < len(line):
    tree = line[(n + 1)]
    can_see.append(tree)
    if heights[tree] >= max_visible:
      break
    n += 1
  return can_see


def visible_from_here(start, heights, fn):
  """Look in all directions from this point, and return which heights are
  visible by whatever visibility function is passed in."""
  # x0y0 x1y0 x2y0 x3y0 x4y0
  # x0y1 x1y1 x2y1 x3y1 x4y1
  # x0y2 x1y2 x2y2 x3y2 x4y2
  # x0y3 x1y3 x2y3 x3y3 x4y3
  # x0y4 x1y4 x2y4 x3y4 x4y4
  startx, starty = start
  visible = []
  score = 1

  sightlines = [
    # Look north: x doesn't change, y decreases
    [(startx, y) for y in range(starty, -1, -1)],
    # Look south: x doesn't change, y increases
    [(startx, y) for y in range(starty, maxy)],
    # Look west: x decreases, y doesn't change
    [(x, starty) for x in range(startx, -1, -1)],
    # Look east: x increases, y doesn't change
    [(x, starty) for x in range(startx, maxx)],
  ]

  for sightline in sightlines:
    found = fn(sightline, heights)
    visible.extend(found)
    score *= len(found)
  return (visible, score)


#########
# Setup1
#########
heights = {}
for y in range (len(lines)):
  for x in range (len(lines[0])):
    heights[(x, y)] = lines[y][x]

#########
# Part 1
#########
# Add all the sides and edges

outsides = set()

for x in range(maxx):
  outsides.add((x, 0))
  outsides.add((x, maxy - 1))
for y in range(maxy):
  outsides.add((0, y))
  outsides.add((maxx - 1, y))

visible = set(outsides)
for start in outsides:
  from_here, _ = visible_from_here(start, heights, look_part_a)
  visible.update(from_here)

print ("Part 1:", len (visible), "heights are visible")

#########
# Part 2
#########
max_score = 0
for start in heights.keys():
  _, score = visible_from_here(start, heights, look_part_b)
  if score > max_score:
    max_score = score

print("Part 2: highest score is", max_score)
