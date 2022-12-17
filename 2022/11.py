#!/usr/bin/env python3
# Advent of code Day 11

import collections
import math
import operator
import re

filename = "input11.txt"
#filename = "test11.txt"
with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

class Monkey(object):
  def __init__(self):
    self.name = ""
    self.has = collections.deque([]) # pop from left, add to right
    self.op = None
    self.val = None
    self.div = None # divisible by...
    self.trueto = None
    self.falseto = None
    self.throwcount = 0

  def add_items(self, items):
    self.has.extend(items)

  def has_items(self):
    if self.has:
      return True
    return False

  def operate(self, item):
    if self.val == "old":
      return self.op(item, item)
    else:
      return self.op(item, int(self.val))

  def set_fn(self, s):
    op_re = "old ([+\-*\/]) (old|\d+)"
    match = re.match(op_re, s)
    ops = {
      "+": operator.add,
      "*": operator.mul,
    }
    self.op = ops[match.groups(1)[0]]
    self.val = match.groups(1)[1]


  def throw(self, part=1):
    "Inspect the item, choose where to throw it."
    item = self.has.popleft()
    self.throwcount += 1
    item = self.operate(item)
    if part == 1:
      item = int(math.floor(item / 3.0))
    #if part == 2:
      # we want to know if the item's divisible by 23, 19, 13 or 17

    if item % self.div == 0:
      return item, self.trueto
    else:
      return item, self.falseto

  def __repr__(self):
    return "Monkey %s, holding %s" % (self.name, self.has)

print (lines)

monkeys = {}

current = None

for line in lines:
  if line == "":
    continue
  if line.startswith("Monkey"):
    name = current = int(line.split("Monkey ")[1].split(":")[0])
    current = Monkey()
    current.name = name
    monkeys[name] = current
  elif line.startswith("Starting items:"):
    current.add_items(
      [int(x.strip()) for x in line.split("Starting items: ")[1].split(",")])
  elif line.startswith("Operation:"):
    current.set_fn(line.split("Operation: new = ")[1])
  elif line.startswith("Test:"):
    current.div = int(line.split("Test: divisible by ")[1])
  elif line.startswith("If true:"):
    current.trueto = int(line.split("If true: throw to monkey ")[1])
  elif line.startswith("If false:"):
    current.falseto = int(line.split("If false: throw to monkey ")[1])
  else:
    print("PARSE ERROR: got", line)
    exit(1)

# Part 1
for round in range (1, 21):
  for i in range(len(monkeys)):
    while monkeys[i].has_items():
      item, who = monkeys[i].throw()
      #print ("Monkey %d throws %d to monkey %d" % (i, item, who))
      monkeys[who].has.append(item)
  #print("* After round", round)
  #for m in monkeys:
  #  print (monkeys[m], monkeys[m].throwcount)

counts = {}
for m in monkeys:
  monkey = monkeys[m]
  counts[m] = monkey.throwcount

actives = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
print ("Part 1", actives[0][1] * actives[1][1])

exit(0)

# Part 2
# TODO: math magic required
for round in range (1, 10001):
  for i in range(len(monkeys)):
    while monkeys[i].has_items():
      item, who = monkeys[i].throw(part=2)
      #print ("Monkey %d throws %d to monkey %d" % (i, item, who))
      monkeys[who].has.append(item)
  print("* After round", round)
  for m in monkeys:
    print (m, monkeys[m].has)

counts = {}
for m in monkeys:
  monkey = monkeys[m]
  counts[m] = monkey.throwcount

actives = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
print (actives[0][1] * actives[1][1])

#

# 13223735010 too high
# 2950025208 too low
# 2713310158 
