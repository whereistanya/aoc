#!/usr/bin/env python3
# Advent of code Day 11

import collections
import math
import operator
import re

test = True
test = False

if test:
  filename = "test11.txt"
else:
  filename = "input11.txt"

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
    self.monkeys = []
    if test:
      self.magic = 23 * 19 * 13 * 17
    else:
      self.magic = 17 * 2 * 5 * 3 * 7 * 13 * 19 * 11

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

    orig = self.has.popleft()
    self.throwcount += 1
    item = self.operate(orig)
    if part == 1:
      item = int(math.floor(item / 3.0))
    else:
      item = item % self.magic

    if item % self.div == 0:
      giveto = self.monkeys[self.trueto]
    else:
      giveto = self.monkeys[self.falseto]

    giveto.has.append(item)

  def __repr__(self):
    return "Monkey %s, holding %s" % (self.name, self.has)

monkeys = {}

current = None

def parse(lines):
  monkeys = {}
  for line in lines:
    if line == "":
      continue
    if line.startswith("Monkey"):
      name = current = int(line.split("Monkey ")[1].split(":")[0])
      current = Monkey()
      current.name = name
      current.monkeys = monkeys
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
  return monkeys

# Part 1
monkeys = parse(lines)
for round in range (1, 21):
  for i in range(len(monkeys)):
    while monkeys[i].has_items():
      monkeys[i].throw()

counts = {}
for m in monkeys:
  monkey = monkeys[m]
  counts[m] = monkey.throwcount

actives = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
print ("Part 1", actives[0][1] * actives[1][1])

# Part 2
monkeys = parse(lines)
for round in range (1, 10001):
  for i in range(len(monkeys)):
    while monkeys[i].has_items():
      monkeys[i].throw(part=2)

counts = {}
for m in monkeys:
  monkey = monkeys[m]
  counts[m] = monkey.throwcount

actives = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
print ("Part 2", actives[0][1] * actives[1][1])

