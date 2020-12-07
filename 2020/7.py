#!/usr/bin/env python
# Day 7

class Bag(object):
  def __init__(self, name):
    self.name = name
    self.contains = {} # {str: count} # TODO: change to Bag?

  def __repr__(self):
    return "Bag(%s -> %s)" % (self.name, self.contains.keys())

inputfile = "input7.txt"

lines = [
  "light red bags contain 1 bright white bag, 2 muted yellow bags",
  "dark orange bags contain 3 bright white bags, 4 muted yellow bags",
  "bright white bags contain 1 shiny gold bag",
  "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags",
  "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags",
  "dark olive bags contain 3 faded blue bags, 4 dotted black bags",
  "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags",
  "faded blue bags contain no other bags",
  "dotted black bags contain no other bags",
]
lines = [
  "shiny gold bags contain 2 dark red bags",
  "dark red bags contain 2 dark orange bags",
  "dark orange bags contain 2 dark yellow bags",
  "dark yellow bags contain 2 dark green bags",
  "dark green bags contain 2 dark blue bags",
  "dark blue bags contain 2 dark violet bags",
  "dark violet bags contain no other bags",
]
with open(inputfile, "r") as f:
  lines = [x.strip().strip(".") for x in f.readlines()]

bags = {}  # {str: Bag, ...}
for line in lines:
  outer_name, contained = line.replace("bags", "").replace("bag", "").strip().split(" contain ")
  outer_name = outer_name.strip()
  if outer_name in bags:
    outer_bag = bags[outer_name]
  else:
    outer_bag = Bag(outer_name)
    bags[outer_name] = outer_bag

  inners = [x.strip() for x in contained.split(",")]
  for inner in inners:
    if inner == "no other":
      continue
    first = inner.split(" ")[0].strip()
    bag_name = inner[len(first):].strip()
    if bag_name not in bags:
      bags[bag_name] = Bag(bag_name)
    count = int(first)
    outer_bag.contains[bag_name] = count

# Part one
seen = set()
can_reach_gold = set(["shiny gold"])

def look_inside(outer): # Bag
  if outer.name in can_reach_gold:
    return True
  for bag_name in outer.contains.keys():
    bag = bags[bag_name]
    if look_inside(bag):
      can_reach_gold.add(outer.name)
      return True
  return False


for bag in bags.values():
  look_inside(bag)

print can_reach_gold
print len(can_reach_gold) - 1

# Part two
def count_inside(outer):
  if not outer.contains:
    return 0
  count = 0
  for bag, number in outer.contains.iteritems():
    count += number
    count += (number * count_inside(bags[bag]))
  return count

current = bags["shiny gold"]
print count_inside(current)
