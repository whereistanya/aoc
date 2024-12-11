#!/usr/bin/env python

filename = "input.txt"
#filename = "test1"
with open(filename, "r") as f:
  line = [int(x) for x in f.read().strip()]


class RepeatingValue(object):
  def __init__(self, count, value):
    self.count = count
    self.value = value

  def __repr__(self):
    return self.value * self.count

# A block group can contain empty space, RepeatingValues, or both.
# The empty space is always to the right of any data.
class BlockGroup(object):
  def __init__(self):
    self.data = []  # [RepeatingValue, ...]
    self.remainingSpace = 0

  def __repr__(self):
    s = "".join([str(x) for x in self.data])
    s += "." * self.remainingSpace
    return "%s" % s


def getNextSpacePos(disk, startFrom):
  i = startFrom
  while True:
    if i >= len(disk):
      return
    if disk[i].remainingSpace > 0:
      return i
    i += 1

# return the position of the rightmost data block starting at some index.
def getNextDataPos(disk, startFrom): # goes backwards
  i = startFrom
  while True:
    if i < 1: # kind of a hack to avoid looking too far; assume there's at least 1 block
      return
    if len(disk[i].data) > 0: # then it's a data block
      return i
    i -= 1

# Find the first empty space that can fit 'count' blocks. Stop looking at some index.
def findSpaceBefore(disk, count, endAt):
  for i in range (endAt):
    if disk[i].remainingSpace >= count:
      return i
  return None

# Reset disk and its blockgroups.
def parse(lines):
  disk = []
  fileIdPos = [] # for part 2
  val = 0
  for i in range (len(line)):
    count = line[i]
    b = BlockGroup()
    if i % 2 == 0: # even blocks are data blocks
      d = RepeatingValue(count, str(val))
      fileIdPos.append(len(disk)) # position we're appendng to
      b.data.append(d)
      val += 1
    else: # odd blocks are space blocks
      if count == 0:
        continue
      b.remainingSpace = count
    disk.append(b)
  return disk, fileIdPos


# Part 1. The number of blockgroups on disk doesn't change: we just move stuff around in them.
disk, _ = parse(line)

nextDataPos = getNextDataPos(disk, len(disk) - 1)
nextSpacePos = getNextSpacePos(disk, 1)

while nextDataPos > nextSpacePos:
  toMoveFrom = disk[nextDataPos]
  assert len(toMoveFrom.data) == 1, "Only expected to move one data block."
  earliestSpace = disk[nextSpacePos]
  fullyMoved = False

  d = toMoveFrom.data[0]

  if earliestSpace.remainingSpace >= d.count: # the whole block can move here
    earliestSpace.data.append(d)
    toMoveFrom.data = []
    earliestSpace.remainingSpace -= d.count
    toMoveFrom.remainingSpace = 1 # We never reuse these files so don't bother about what size they should be,
    fullyMoved = True

  else:  # only part of the block can move here; split the block
    newd = RepeatingValue(earliestSpace.remainingSpace, d.value)
    d.count -= earliestSpace.remainingSpace
    earliestSpace.remainingSpace = 0
    earliestSpace.data.append(newd)

  if earliestSpace.remainingSpace == 0:
    nextSpacePos = getNextSpacePos(disk, nextSpacePos)
  if fullyMoved:
    nextDataPos = getNextDataPos(disk, nextDataPos)


i = 0
part1 = 0
for bg in disk:
  blocks = bg.data
  for block in blocks:
    for j in range(block.count):
      part1 += i * int(block.value)
      i += 1

print("Part 1:", part1)

# Part2. Full reset of disk and blocks.
disk, fileIdPos = parse(line)

# try moving each file once
for posToMove in fileIdPos[::-1]: # backwards through data blocks
  toMoveFrom = disk[posToMove]
  assert len(toMoveFrom.data) == 1, "Only expected to move one data block."

  nextSpacePos = findSpaceBefore(disk, toMoveFrom.data[0].count, posToMove)
  if not nextSpacePos:
    continue
  earliestSpace = disk[nextSpacePos]

  d = toMoveFrom.data[0]
  earliestSpace.data.append(d)
  toMoveFrom.data = []
  toMoveFrom.remainingSpace = d.count
  earliestSpace.remainingSpace -= d.count

i = 0
part2 = 0
for bg in disk:
  blocks = bg.data
  for block in blocks:
    for j in range(block.count):
      part2 += i * int(block.value)
      i += 1
  if bg.remainingSpace > 0:
    i += bg.remainingSpace

print("Part 2:", part2)
