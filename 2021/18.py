#!/usr/bin/env python

inputfile = "input.txt"
with open(inputfile, "r") as f:
  lines = [x.strip() for x in f.readlines()]

import math

class Pair(object):
  def __init__(self, s, parent=None):
    self.base_string = s
    self.left = None   # Pair or None
    self.right = None  # Pair or None
    self.parent = parent  # Pair or None
    self.value = -1  # int or -1
    self.parse()
    self.depth = -1


  def parse(self):
    #print("parsing", self.base_string)

    # It's a value
    if not any(x in self.base_string for x in [",", "[", "]"]):
      self.value = int(self.base_string)
      return

    # Otherwise, strip off the outer []s
    to_parse = self.base_string[1:-1]
    stack = []
    left = ""
    for i in range(len(to_parse)):
      char = to_parse[i]
      if char == "," and len(stack) == 0:  # empty stack => middle
        self.left = Pair(left, parent=self)
        self.right = Pair(to_parse[i+1:], parent=self)
      else:
        left += char
        if char == "[":
          stack.append(char)
        elif char == "]":
          stack.pop()

  def __repr__(self):
    """
    if self.value >= 0:
      s = "%d(%d)" % (self.value, self.depth)
    else:
      s = "[%s,%s(%d)]" % (self.left, self.right, self.depth)
    """
    if self.value >= 0:
      s = "%d" % (self.value)
    else:
      s = "[%s,%s]" % (self.left, self.right)
    return s

  def magnitude(self):
    if self.value >= 0:
      return self.value
    return ((self.left.magnitude() * 3) +
            (self.right.magnitude() * 2))

  def traverse(self, ordered, depth=0):
    """node, left,right"""
    self.depth = depth
    #print("traverse(%s, %d)" % (ordered, depth))
    if self.value >= 0:
      ordered.append(self)
      return

    self.left.traverse(ordered, depth + 1)
    self.right.traverse(ordered, depth + 1)


  def explode(self):
    self.left.parent = None  # TODO: unnecessary?
    leftvalue = self.left.value
    self.left = None
    self.right.parent = None
    rightvalue = self.right.value
    self.right = None
    self.value = 0
    return leftvalue, rightvalue

  def add_left(self, value, seen):
    if self.value >= 0:
      self.value += value

  def add_right(self, value, seen):
    if self.value >= 0:
      self.value += value

  def split(self):
    self.left = Pair("%d" % math.floor(self.value / 2.0), parent=self)
    self.right = Pair("%d" % math.ceil(self.value / 2.0), parent=self)
    self.value = -1


def reduce(start):
  #print "Reducing", start

  while True:
    found = False
    # walk through the nodes until you find something at depth
    # 4 or value > 10.
    ordered = []

    start.traverse(ordered, 0)

    for i in range(len(ordered)):
      node = ordered[i]
      # If node depth is 4, explode the node.
      # But we're only storing the nodes with values, so look one deeper and
      # explore the parent node instead. So moving forward 2 not 1 for
      # addright. Not sure it works. If there's a bug, it's here.
      if node.depth == 5:
        #print("Explode %s" % node.parent)
        if node.parent.depth != 4:
          print "BUG"
          exit()
        addleft, addright = node.parent.explode()
        if i != 0:
          ordered[i - 1].value += addleft
        if i != (len(ordered) - 2):
          ordered[i + 2].value += addright
        found = True
        break
    if not found:
      for i in range(len(ordered)):
        node = ordered[i]
        if node.value >= 10:
        #  print("Split %s" % node)
          node.split()
          found = True
          break
    if not found:
      return

def add(a, b):
  """Add two Pairs

  Args:
    a, b: Pair
  Returns:
    (Pair): new Pair with a and b as left and right
  """
  # Could do [%s,%s] % (a, b) instead
  pair = Pair("[%s,%s]" % (a, b)) # TODO parent
  reduce(pair)
  return pair

def test():
  lines = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split("\n")
  return lines

#lines = test()

# Part1
result = str(add(lines[0], lines[1]))

# Re-parsing everything every time. Would be more efficient to slot in a
# new parent node. But this works.
for i in range(2, len(lines)):
  final = add(result, lines[i])
  result = str(final)

print final.magnitude()

# Part2
biggest = 0

for i in range(0, len(lines)):
  for j in range(0, len(lines)):
    if i == j:
      continue
    print i,j
    magnitude = add(lines[i], lines[j]).magnitude()
    if magnitude > biggest:
      biggest = magnitude
print biggest

