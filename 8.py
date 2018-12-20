#!/usr/bin/env python
# Advent of code Day 8.

import string
import sys

with open("day8input.txt", "r") as f:
  line = f.read().strip()

#line = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

numbers = [int(x) for x in line.split()]

"""
The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is 10+11+12=33, and the value of node D is 99.

However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. The value of this node is the sum of the values of the child nodes referenced by the metadata entries. If a referenced child node does not exist, that reference is skipped. A child node can be referenced multiple time and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.
"""

class Node(object):
  def __init__(self):
    self.children = [] # [Node, Node]
    self.expected_children = 0  # int
    self.expected_metadata = 0 # int
    self.parent = None  # Node
    self.metadata = [] # [int, ...]

  def value(self):
    if self.expected_children == 0:
      return sum(self.metadata)
    total = 0
    for meta in self.metadata:
      if meta > len(self.children):
        continue
      total += self.children[meta - 1].value() # -1 because zero indexing.
    return total

  def __repr__(self):
    return "(Node: %d/%d, %d/%d) -> %s" % (
    len(self.children), self.expected_children,
    len(self.metadata), self.expected_metadata, self.parent)

nodes_open = []

# Fake node to hook everything onto.
root = Node()
root.expected_children = 1  # the whole strip
index = 0
metadata_sum = 0

parent = root

while True:
  if index >= len(numbers):
    #print "And we're done"
    break
  #print "Current parent is", parent
  # if the parent node has all its children, this is its metadata
  if parent.expected_children == len(parent.children):
    parent.metadata = [int(x) for x in numbers[index: index + parent.expected_metadata]]
    index += parent.expected_metadata
    metadata_sum += sum(parent.metadata)
    # now this node is done, so move up one.
    parent.parent.children.append(parent)
    parent = parent.parent
    #print "1. End of a node!", node
    continue

  # Otherwise, look for its children. Read two chars and start at a new node
  node = Node()
  node.parent = parent
  node.expected_children = int(numbers[index])
  node.expected_metadata = int(numbers[index + 1])
  #print "New node with %d, %d" % (node.expected_children, node.expected_metadata)
  index += 2

  if node.expected_children - len(node.children) == 0:
    # metadata starts here
    node.metadata = [int(x) for x in numbers[index: index +
    node.expected_metadata]]
    metadata_sum += sum(node.metadata)
    index += node.expected_metadata
    parent.children.append(node)
    #print "2. End of a node!", node
    # this node is now done. We will not think of it again.
    continue

  # So this node has some children. It becomes the parent, until we find them.
  parent = node

print "Part one:", metadata_sum
print "Part two:", root.children[0].value()
# not 0
