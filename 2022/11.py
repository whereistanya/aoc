#!/usr/bin/env python3
# Advent of code Day 11

with open("test11.txt", "r") as f:
#with open("input11.txt", "r") as f:
  lines = [x.strip() for x in f.readlines()]

class Monkey(object):
  def __init__(self):
    name = ""
    has = []
    fn = None
    test = None # divisible by...
    trueto = None
    falseto = None

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
    current.has = [x.strip() for x in line.split("Starting items: ")[1].split(",")]
  elif line.startswith("Operation:"):
    current.fn = line.split("Operation: new = ")[1]
  elif line.startswith("Test:"):
    current.test = int(line.split("Test: divisible by ")[1])
  elif line.startswith("If true:"):
    current.trueto = int(line.split("If true: throw to monkey ")[1])
  elif line.startswith("If false:"):
    current.falseto = int(line.split("If false: throw to monkey ")[1])
  else:
    print("PARSE ERROR: got", line)
    exit(1)

for m in monkeys:
  print (monkeys[m], monkeys[m].test)
