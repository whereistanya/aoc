#!/usr/bin/env python3

test = True
test = False

if test:
  filename = "test20.txt"
else:
  filename = "input20.txt"

with open(filename, "r") as f:
  numbers = [int(x.strip()) for x in f.readlines()]

class Node(object):
  def __init__(self, val):
    self.val = val
    self.prev = None
    self.next = None

  def __repr__(self):
    return "Node(%d)  [%d]<- ->[%d]" % (self.val, self.prev.val, self.next.val)

ordered = {}
zero_node = None

part = 2

if part == 2:
  key = 811589153
  mixes = 10
else:
  key = 1
  mixes = 1

for i in range(len(numbers)):
  number = numbers[i]
  node = Node(number * key)
  ordered[i] = node
  if number == 0:
    zero_node = node
size = len(ordered)

for i in range(len(numbers)):
  node = ordered[i]
  node.next = ordered[(i + 1) % size]
  node.prev = ordered[(i - 1) % size]

head = ordered[0]

for n in range(mixes):
  for i in range (len(ordered)):
    node = ordered[i]
    new_next = node.next
    to_move = (node.val % (size - 1)) # makes it always positive

    for n in range(to_move % size):
      new_prev = new_next
      new_next = new_next.next

    if to_move > 0:
      orig_next = node.next
      orig_prev = node.prev
      node.next = new_next
      node.prev = new_prev
      new_prev.next = node
      new_next.prev = node
      orig_prev.next = orig_next
      orig_next.prev = orig_prev

to_find = [1000, 2000, 3000]
total = 0

for nth in to_find:
  node = zero_node
  for n in range(nth % size):
    node = node.next
  total += node.val

print("Part %d: %d" % (part, total))
