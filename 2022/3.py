#!/usr/bin/env python3
# Advent of code Day 3

#with open("test3.txt", "r") as f:
with open("input3.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

def score(c):
  if c.isupper():
    return ord(c) - 38
  elif c.islower():
    return ord(c) - 96
  else:
    print("BUG: got", c)
    exit(1)

# Tests
assert(score('a') == 1)
assert(score('A') == 27)

total = 0

for line in lines:
  half = int(len(line) / 2)
  first = line[0:half]
  second = line[half:]
  overlap = set([x for x in first]) & set([x for x in second])
  if len(overlap) != 1:
    print ("BUG: length was", len(overlap))
    exit(1)
  total += score(overlap.pop())

print("Part 1", total)


total = 0
groups = [ lines[i:i + 3] for i in range(0, len(lines), 3)]

for group in groups:
  found = {}
  for inventory in group:
    print(inventory)
    for c in set(list(inventory)):
      try:
        found[c] += 1
      except KeyError:
        found[c] = 1
  badge = ([x for x, count in found.items() if count == 3])
  if len(badge) != 1:
    print ("BUG: ", badge)
    exit(1)
  total += score(badge.pop())
print("Part 2", total)

