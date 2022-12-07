#!/usr/bin/env python3


class Node(object):

  def __init__(self):
    self.links = {}
    self.name = "" # useful for debugging; not actually needed
    self.children = []
    self.weight = 0

  def dirsize(self):
    if len(self.children) == 0:
      return self.weight
    else:
      return sum([x.dirsize() for x in self.children])

with open("input7.txt", "r") as f:
#with open("test7.txt", "r") as f:
  lines = f.readlines()[1:] # drop the 'cd /'; so lazy

root = Node()
current_node = root
current_node.name = "/"

i = 0

dirs = []

while i < len(lines):
  line = lines[i].strip()
  # Assume we've already created all children on ls, and wired
  # up the parent directory too.
  if line.startswith ("$ cd"):
    rootname = line.split()[-1]
    new_node = current_node.links[rootname]
    current_node = new_node
    i += 1
  elif line.startswith ("$ ls"):
    while (i + 1) < len(lines) and not lines[i + 1].startswith("$"):
      i += 1
      direntry = lines[i].strip()
      if direntry.startswith("dir"):
        dirname = direntry.split()[-1]
        new_node = Node()
        new_node.links[".."] = current_node
        new_node.name = dirname
        current_node.links[dirname] = new_node
        current_node.children.append(new_node)
        dirs.append(new_node) # lazy for part 1
      else:
        weight, name = direntry.split()
        new_node = Node()
        new_node.weight = int(weight)
        new_node.name = name
        current_node.children.append(new_node)
    i += 1

part1_total = 0
for d in dirs:
  dirweight = d.dirsize()
  if dirweight <= 100000:
    part1_total += dirweight

print ("Part 1", part1_total)

available = 70000000 - root.dirsize()
to_find = 30000000 - available
best_so_far = 10000000000
for d in dirs:
  dirweight = d.dirsize()
  if dirweight >= to_find:
    if dirweight < best_so_far:
      best_so_far = dirweight
print("Part 2", best_so_far)
