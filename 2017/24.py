#!/usr/bin/env python
# Advent of code 2017 day 24

class Graph(object):
  def __init__(self):
    self.ends = {} # str: set()
    self.nodes = [] # [Node, Node...]
    self.start_node = None

  def parse(self, lines):
    """Create all of the nodes. Each one has edges of all other nodes who share
    an end."""
    for line in lines:
      end1, end2 = line.strip().split("/")
      name = "%s_%s" % (end1, end2)
      node = Node(name, end1, end2)
      self.nodes.append(node)
      try:
        self.ends[end1].add(node)
      except KeyError:
        self.ends[end1] = set([node])
      try:
        self.ends[end2].add(node)
      except KeyError:
        self.ends[end2] = set([node])

  def find_best_path(self, so_far, end):
    """Recursively find all possible paths.

    Args:
      so_far: nodes we've traversed
      end: (int) number we're looking for next
    Returns:
      (Path): the highest weight path found from here.
    """
    weights = 0
    to_check = []  # list of lists [ [ Node, ...], [Node, ...] ... ]

    edges = self.ends[end]
    for edge in edges:
      if edge not in so_far:
        new_list = list(so_far)
        new_list.append(edge)
        to_check.append((new_list, edge.other_end(end)))
    if not to_check:  # nothing to add; return the final list
      return Path(list(so_far)) # todo does this need the explicit copy

    paths = []
    for path, end in to_check:
      paths.append(self.find_best_path(path, end))
    heaviest = sorted(paths)[-1]
    return heaviest

  def __repr__(self):
    s = ""
    for node in self.nodes:
      s += "%s\n" % node
    return s


class Path(object):
  def __init__(self, path):
    self.path = path # [Node, ...]
    self.length = len(path)
    self.weight = 0
    for node in self.path:
      self.weight += node.weight

  def __repr__(self):
    return "%s(%d)" % (self.path, self.weight)

  def __cmp__(self, other):
    # PART2 only:
    if self.length < other.length:
      return -1
    if self.length > other.length:
      return 1
    # END PART2 only
    # Same length; use weight
    if self.weight < other.weight:
      return -1
    if self.weight > other.weight:
      return 1
    return 0

class Node(object):
  def __init__(self, name, end1, end2):
    self.edges = set()
    self.name = name
    self.end1 = end1 # str
    self.end2 = end2 # str
    self.weight = int(end1) + int(end2)

  def other_end(self, end):
    if end == self.end1:
      return self.end2
    elif end == self.end2:
      return self.end1
    else:
      print "Unexpected end %s for node %s/%s" % (end, self.end1, self.end2)
      exit()

  def __repr__(self):
    return self.name

lines = [
	"0/2",
	"2/2",
	"2/3",
	"3/4",
	"3/5",
	"0/1",
	"10/1",
	"9/10",
]

with open("input24.txt", "r") as f:
  lines = f.readlines()

graph = Graph()
graph.parse(lines)

best = graph.find_best_path([], "0")
print "Path:", best.path
print "Weight", best.weight
print "Length", best.length
