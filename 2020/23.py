#!/usr/bin/env python
# AoC 2020 day 23.

class Cup(object):
  def __init__(self, label):
    self.label = label
    self.next = None

  def __repr__(self):
    return "[%s->%s]" % (self.label, self.next.label)

class Circle(object):
  def __init__(self):
    self.current = None  # Cup
    self.moves = 0
    self.cups = {}  # label: Cup
    self.meximum = 0

  def __repr__(self):
    if len(self.cups) > 1000:
      return "Circle with %d cups and current index %s" % (
        len(self.cups), self.current.label)

    cup = self.current
    s = ""
    for i in range(self.maximum):
      s += "%s" % (cup.label)
      cup = cup.next
    return s


  def move(self):
    #print ("- - Move %d - - " % self.moves)
    cup1 = self.current.next
    cup2 = cup1.next
    cup3 = cup2.next

    self.current.next = cup3.next # Remove them

    destinationLabel = self.current.label - 1
    if destinationLabel <= 0:
      destinationLabel = self.maximum
    while destinationLabel in [cup1.label, cup2.label, cup3.label]:
      destinationLabel -= 1
      if destinationLabel <= 0:
        destinationLabel = self.maximum
    destinationCup = self.cups[destinationLabel]

    afterDest = destinationCup.next
    destinationCup.next = cup1
    cup3.next = afterDest

    self.current = self.current.next
    self.moves += 1

# Main

# Real data
initial = "784235916"

# Test data
#initial = "389125467"

labels = [int(x) for x in initial]

circle = Circle()
circle.current = Cup(labels[0])
circle.cups[labels[0]] = circle.current
previous = circle.current

# Initialise the part 1 data
for i in range(1, 9):
  cup = Cup(labels[i])
  circle.cups[labels[i]] = cup
  previous.next = cup
  previous = cup

previous.next = circle.current
circle.maximum = len(circle.cups)

for i in range(11):
  circle.move()

print ("Part 1: %s" % circle)

# Part 2
# Reset
circle.cups = {}
circle.current = Cup(labels[0])
circle.cups[labels[0]] = circle.current
previous = circle.current

for i in range(1, 9):
  cup = Cup(labels[i])
  circle.cups[labels[i]] = cup
  previous.next = cup
  previous = cup

for i in range(10, 1000001):
  cup = Cup(i)
  circle.cups[i] = cup
  previous.next = cup
  previous = cup

previous.next = circle.current
circle.maximum = len(circle.cups)

for i in range(10000001):
  circle.move()

print ("Part 2: %d" % (
  circle.cups[1].next.label * circle.cups[1].next.next.label))

