#!/usr/bin/env python
# Advent of code Day 7

import collections
import re

class Node(object):
  def __init__(self, name, weight):
    self.name = name
    self.weight = weight
    self.aggregate_weight = -999
    self.above = []  # [Node, ...]
    self.below = []  # [Node, ...]

  def total_weight(self):
    # unnecessary optimisation wooo
    if self.aggregate_weight != -999:
      return self.aggregate_weight

    weight = self.weight
    for above in self.above:
      weight += above.total_weight()
    self.aggregate_weight = weight
    return weight

  def __repr__(self):
    return "%s(%d): [%d] [%d]" % (self.name, self.weight,
                                  len(self.above), len(self.below))


with open("input7.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
  "pbga (66)",
  "xhth (57)",
  "ebii (61)",
  "havc (66)",
  "ktlj (57)",
  "fwft (72) -> ktlj, cntj, xhth",
  "qoyq (66)",
  "padx (45) -> pbga, havc, qoyq",
  "tknk (41) -> ugml, padx, fwft",
  "jptl (61)",
  "ugml (68) -> gyxo, ebii, jptl",
  "gyxo (61)",
  "cntj (57)",
]
"""

line_re = "(\w+) \((\d+)\)( -> )?(.*)?$"

nodes = {}

for line in lines:
  groups = re.search(line_re, line).groups()
  name = groups[0]
  weight = int(groups[1])
  if name in nodes:
    node = nodes[name]
    node.weight = weight
  else:
    node = Node(name, weight)
    nodes[name] = node

  try:
    above_nodes = groups[3].split(",")
    for above_name in above_nodes:
      above_name = above_name.strip()
      if above_name == "": # TODO: fix these
        continue
      if above_name in nodes:
        above_node = nodes[above_name]
      else:
        above_node = Node(above_name, -999)  # default value
        nodes[above_name] = above_node
      node.above.append(above_node)
      above_node.below.append(node)
  except IndexError:
    pass

# Last pass to find the ones with no below nodes

root_node = None
for node_name in nodes:
  node = nodes[node_name]
  if not node.below:
    print "Part 1:",  node
    root_node = node

#assert nodes["ugml"].total_weight() == 251
#assert nodes["padx"].total_weight() == 243
#assert nodes["fwft"].total_weight() == 243

print "Part 2:"
to_check = collections.deque()
to_check.append(root_node)

last_even = None

while to_check:
  node = to_check.popleft()
  weights = set()
  for above in node.above:
    weights.add(above.total_weight())
  if len(weights) > 1:
    last_uneven = node
    for above in node.above:
      to_check.append(above)

print last_uneven
weights = {}
for above in last_uneven.above:
  #print " => ", above.name, above.total_weight(), above.weight

  if above.total_weight() in weights:
    weights[above.total_weight()].append(above.name)
  else:
    weights[above.total_weight()] = [above.name]
print weights

print "Adjust the actual (not aggregate) weight of whichever one is different"
print "I have to go eat indian food now but maybe I'll write this some time"
