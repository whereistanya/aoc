#!/usr/bin/env python


class Circle(object):
  def __init__(self, initial):
    self.values = [int(x) for x in initial] # ??increases in size, we X out removed things
    self.current = 0
    self.moves = 1
    self.minimum = min(self.values)
    self.maximum = max(self.values)

  def getByIndex(self, index):  # Returns a label
    return self.values[(index % len(self.values))]

  def getByLabel(self, value):  # Returns an index
    for i in range(len(self.values)):
      if self.values[i] == value:
        return i
    print ("ERROR: didn't find %d" % value)

  def addAtIndex(self, index, value):
    self.values.insert(index, value)
  
  def moveForwardsFrom(self, index): # Returns an index
    forward = index + 1
    if forward >= len(self.values):
      forward = 0
    return forward

  def minusOne(self, value):
    smaller = value - 1
    if smaller < self.minimum:
      smaller = self.maximum
    return smaller

  """
  def deleteByIndexes(self, indexes):
    indexesToDelete = []
    for index in indexes:
      indexesToDelete.append(index % len(self.values))
    print "deleting", sorted(indexesToDelete)[::-1]
    for index in sorted(indexesToDelete)[::-1]:
      print "deleting index", index
      del(self.values.remove(index)
      print "now have", self.values
   """

  def moveBackFrom(self, index): # Returns an index
    back = index - 1
    if back < 0:
      back = len(self.values) - 1
    return back

  def move(self):
    print ("- - Move %d - - " % self.moves)
    # edits cups in place
    currentIndex = self.current
    currentValue = self.getByIndex(currentIndex)
    print ("Cups: %s" % self.values)
    print ("Current: %d" % currentValue)
    toMove = [self.getByIndex(x) for x in [currentIndex + 1, currentIndex + 2,
                                           currentIndex + 3]]
    print ("Pick up %s" % toMove)
    for number in toMove:
      self.values.remove(number)
    #self.deleteByIndexes([currentIndex + 1, currentIndex + 2, currentIndex + 3])
    print ("Postdel: %s" % self.values)

    destinationValue = self.minusOne(currentValue)
    while (destinationValue in toMove):
      print("Moving back from %d" % destinationValue)
      destinationValue = self.minusOne(destinationValue)
    destinationIndex = self.getByLabel(destinationValue)
    print ("Destination: %d at index %d" % (destinationValue, destinationIndex))

    for i in range(1, len(toMove) + 1):
      self.addAtIndex(destinationIndex + i, toMove[i - 1])
      
    currentIndex = self.getByLabel(currentValue)
    self.current = self.moveForwardsFrom(currentIndex)
    self.moves += 1


  def __repr__(self):
    return ",".join([str(x) for x in self.values])

# Real data
initial = "784235916"

# Test data
initial = "389125467"

circle = Circle(initial)
for i in range(100):
  print(circle)
  circle.move()

listPieces = "".join([str(x) for x in circle.values]).split("1")
part1 = listPieces[1] + listPieces[0]

print(part1)


