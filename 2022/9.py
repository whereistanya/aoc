#!/usr/bin/env python3
# Advent of code Day 9

#with open("test9b.txt", "r") as f:
with open("input9.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

def move(first, d):
  x, y = first
  match d:
    case 'U':
      return x, y - 1
    case 'D':
      return x, y + 1
    case 'L':
      return x - 1, y
    case 'R':
      return x + 1, y
    case _:
      print("BUG: got", d)

def touching(first, second):
  x1, y1 = first
  x2, y2 = second
  if ((abs(x1 - x2) < 2) and
      (abs(y1 - y2) < 2)):
    return True
  return False

def move_towards(first, second):
  """Move x1, y1 towards x2, y2"""
  x1, y1 = first
  x2, y2 = second
  if y1 > y2:
    y1 -= 1
  elif y1 < y2:
    y1 += 1
  #if y1 == y2:
  if x1 > x2:
    x1 -= 1
  elif x1 < x2:
    x1 += 1
  return x1, y1

def move_knots(knot_count):
  pos = [(0, 0) for x in range(knot_count)]
  visits = set([pos[-1]])

  for line in lines:
    direction, count = line.split()
    count = int(count)
    for i in range (count):
      pos[0] = move(pos[0], direction)
      for k in range(0, knot_count - 1):
        if not touching(pos[k], pos[k + 1]):
          pos[k + 1] = move_towards(pos[k + 1], pos[k])
      visits.add(pos[-1]) # tail
  return len(visits)


print("Part 1:", move_knots(2))
print("Part 2:", move_knots(10))
