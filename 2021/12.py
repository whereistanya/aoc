#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

def test1():
  return """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n")

def test2():
  return """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split("\n")

def test3():
  return """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split("\n")

lines = test1()
print (lines)

class Cave(object):
  def __init__(self, name):
    self.name = name
    if name[0].isupper():
      self.size = "big"
    else:
      self.size = "small"
    self.edges = set()

  def __repr__(self):
    return "Cave %s(%s): exit to %s" % (self.name, self.size, [x.name for x in self.edges])

caves = {} # str:Cave

for line in lines:
  a,b = line.split("-")
  if a in caves:
    end1 = caves[a]
  else:
    end1 = Cave(a)
    caves[a] = end1
  if b in caves:
    end2 = caves[b]
  else:
    end2 = Cave(b)
    caves[b] = end2
  end1.edges.add(end2)
  end2.edges.add(end1)

for cave in caves.values():
  print(cave)
print()

def move(a, seen):
  if a.name == "end":
    print "end!", seen
    return 1
  edges = a.edges
  paths_from_here = 0
  for edge in edges:
    if edge.name in seen and edge.size == "small":
      continue
    seen.append(edge.name)
    paths_from_here += move(edge, seen)
    seen.pop()
  return paths_from_here

start = caves["start"]
print(move(start, ["start"]))

