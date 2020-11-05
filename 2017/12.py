#!/usr/bin/env python

import collections

class Node(object):
  def __init__(self, name):
    self.name = name
    self.edges = set()  # set([Node, ...])

  def __repr__(self):
    return "%s: %d edges" % (self.name, len(self.edges))

with open("input12.txt", "r") as f:
  lines = f.readlines()

"""lines = [
  "0 <-> 2",
  "1 <-> 1",
  "2 <-> 0, 3, 4",
  "3 <-> 2, 4",
  "4 <-> 2, 3, 6",
  "5 <-> 6",
  "6 <-> 4, 5",
]"""

nodes = {}
for line in lines:
  start, endstr = line.strip().split(" <-> ")
  ends = [x.strip() for x in endstr.split(",")]

  if start in nodes:
    startnode = nodes[start]
  else:
    startnode = Node(start)
    nodes[start] = startnode

  for end in ends:
    if end in nodes:
      endnode = nodes[end]
    else:
      endnode = Node(end)
      nodes[end] = endnode

    startnode.edges.add(endnode)
    endnode.edges.add(startnode)


def nodes_from(start):
  to_check = collections.deque()
  to_check.append(start)
  seen = set()
  while to_check:
    node = to_check.popleft()
    if node.name in seen:
      continue
    seen.add(node.name)
    for edge in node.edges:
      if edge.name not in seen:
        to_check.append(edge)
  return seen



print "Part 1"

startnode = nodes["0"]
seen = nodes_from(startnode)
print len(seen)

print "Part 2"
all_nodes = set(nodes)

for node in seen:
  all_nodes.remove(node)

groups = 1
while all_nodes:
  startnode = all_nodes.pop()

  found = nodes_from(nodes[startnode])
  groups += 1

  for nodename in found:
    if nodename != startnode: # hack because set doesn't have a peek() method
      all_nodes.remove(nodename)

print groups
