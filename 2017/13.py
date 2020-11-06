#!/usr/bin/env python


class Scanner(object):
  def __init__(self, depth, scanrange):
    self.depth = depth
    self.position = 1
    self.scanrange = scanrange
    self.direction = "down"
    self.at_top = set()

  def __repr__(self):
    return "%s (%d/%d)" % (self.depth, self.position, self.scanrange)

  def reset(self):
    self.position = 1
    self.direction = "down"

  def move(self, times=1):
    for i in range(times):
      if self.direction == "down":
        self.position += 1
      else:
        self.position -= 1
      if self.direction == "up" and self.position == 1:
        self.direction = "down"
      elif self.direction == "down" and self.position == self.scanrange:
        self.direction = "up"

  def calculate_locations(self):
    self.at_top.add(0)
    i = 0
    while True:
      i += 2 * (self.scanrange - 1)
      self.at_top.add(i)
      if i > 5000000:
        break


with open("input13.txt", "r") as f:
  lines = f.readlines()

"""
lines = [
"0: 3",
"1: 2",
"4: 4",
"6: 4",
]
#"""

scanners = {}
for line in lines:
  values = [x.strip() for x in line.strip().split(":")]
  scanners[int(values[0])] = Scanner(int(values[0]), int(values[1]))
  scanners[int(values[0])].calculate_locations()

print scanners

delay = 0 # Delay is 0 for part 1

while True:
  severity = 0
  caught = False

  for position in range(0, 100):
    if (position) in scanners:
      scanner = scanners[position]
      #if scanner.position == 1:
      #  print delay, "Caught at layer", position
      #  caught = True
      #  severity += (scanner.depth * scanner.scanrange)
      if (position + delay) in scanner.at_top:
        #print "Caught at layer", position
        caught = True
        severity += (scanner.depth * scanner.scanrange)
        break
    #for name, scanner in scanners.iteritems():
    #  scanner.move()
  #print "Delay", delay, "=>", severity
  if not caught:
    print "Breaking at delay", delay
    break
  delay += 1
  #break # just run once for now

print "Part 1", severity


