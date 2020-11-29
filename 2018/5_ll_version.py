#!/usr/bin/env python
# Advent of code Day 2.

import sys

with open("day5input.txt", "r") as f:
  line = f.read().strip()

# line = "dabAcCaCBAcCcaDA"

#######################################################
# Part one
#######################################################

class Node(object):
  def __init__(self, value, previous_node):
    self.value = value
    self.previous_node = previous_node
    self.next_node = None

  def __repr__(self):
    if self.next_node is None:
      return self.value
    return "%s->%s" % (self.value, self.next_node)

  def next_value(self):
    if self.next_node is None:
      return None
    return self.next_node.value

  def int_value(self):
    return ord(self.value)

  def int_next_value(self):
    return ord(self.next_value())

class DoublyLinkedList(object):
  def __init__(self):
    self.head = None
    self.tail = None
    self.count = 0

  def delete(self, node):
    self.count -= 1
    if node.next_node and node.previous_node:
      node.previous_node.next_node = node.next_node
      node.next_node.previous_node = node.previous_node
    #else:
    #  node.previous_node.next_node = None

    #  node.next_node.previous_node = node.previous_node
    #else:
    #  node.next_node.previous_node = None

  def insert_right(self, value):
    self.count += 1
    if self.tail == None:  # first node
      new_node = Node(value, None)
      self.head = new_node
      self.tail = new_node
      return
    new_node = Node(value, self.tail)
    new_node.previous_node = self.tail
    self.tail.next_node = new_node
    self.tail = new_node

  def __repr__(self):
    return "%d nodes: %s" % (self.count, head)

  def printlist(self):
    node = head
    s = ""
    while node != None:
      s += node.value
      node = node.next_node
    print(s)

DISTANCE = 32  # Distance between A' and 'a' in ascii table.

ll = DoublyLinkedList()
for char in line:
  ll.insert_right(char)

head = ll.head # first node
changes = False
node = head
print("Count is %d" % ll.count)

while True:
  if node is None or node.next_node is None: # last node
    if not changes:
      break
    node = head
    changes = False

  if abs(node.int_value() - node.int_next_value()) == DISTANCE:
    changes = True
    ll.delete(node.next_node)
    new = node.next_node
    ll.delete(node)
    node = new
    continue
  node = node.next_node


print("list is now", ll.count)
