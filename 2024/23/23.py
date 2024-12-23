#!/usr/bin/env python

import sys
sys.path.append("../../")
import util.grid as gridlib

from collections import defaultdict

filename = "input.txt"
#filename = "test1"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

part1 = 0
part2 = 0

connections = set()
allnodes = set()
trios = set()

links = defaultdict(set)



for line in lines:
  first, second = line.split("-")
# part1
  connections.add( (first, second))
  connections.add( (second, first))
  allnodes.add(first)
  allnodes.add(second)
# part2
  links[first].add(second)
  links[second].add(first)
  links["startnode"].add(first)
  links["startnode"].add(second)

for a, b in connections:
  for c in allnodes:
    if (a, c) in connections and (b, c) in connections:
      if a.startswith("t") or b.startswith("t") or c.startswith("t"):
        s = sorted([a, b, c])
        trios.add((s[0], s[1], s[2]))

print(trios)
part1 = len(trios)


# part2
# add one node at a time
def find_connected(start, allnodes, links, seen, ignore, bestSoFar, bestGroup):
  if len(links[start]) < bestSoFar:
    return -1

  toCheck = []
  for node in links[start]:
    if node in ignore:
      continue
    if len(links[node]) < bestSoFar:
      continue
    if node in seen:
      continue
    connected = True
    for pastnode in seen:
      if pastnode not in links[node]:
        connected = False
        break
    if not connected:
      continue
    toCheck.append(node)

  if len(toCheck) == 0:
    #print("path", seen, len(seen))
    if len(seen) > bestSoFar:
      bestGroup = set(seen)
      bestSoFar = len(seen)
      print("part 2: best group so far is", ",".join(sorted(bestGroup)))
    return len(seen) # biggest the set got

  bestThisWay = len(seen)
  for node in toCheck:
    # it's connected to everything that went before so...
    seen.add(node)
    count = find_connected(node, allnodes, links, seen, ignore, bestSoFar, bestGroup)
    if count > bestSoFar:
      bestSoFar = count
    if count > bestThisWay:
      bestThisWay = count
    seen.remove(node)
    ignore.add(node) # don't bother trying this node again in this direction

  return bestThisWay

bestGroup = set()
i = 0
for startnode in allnodes:
  part2 = find_connected(startnode, allnodes, links, set(), set(), part2, bestGroup)
  i += 1


print("Part 1:", part1)
