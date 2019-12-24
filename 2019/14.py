#!/usr/bin/env python
# Advent of code Day 14

import collections
import math
import sys

class Chemical(object):
  def __init__(self, chemical):
    self.name = chemical
    self.needed_by = set()
    self.creates = -1
    self.needed = 0 # How many of these things do we need
    self.needs = [] # all our needs
 
  def __repr__(self):
    return "%s (needed by %d things)" % (self.name, len(self.needs))

with open("input.txt", "r") as f:
  lines = f.readlines()

# Test 5
"""
lines = [
"171 ORE => 8 CNZTR",
"7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
"114 ORE => 4 BHXH",
"14 VRPVC => 6 BMBT",
"6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
"6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
"15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
"13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
"5 BMBT => 4 WPTQ",
"189 ORE => 9 KTJDG",
"1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
"12 VRPVC, 27 CNZTR => 2 XDBXC",
"15 KTJDG, 12 BHXH => 5 XCVML",
"3 BHXH, 2 VRPVC => 7 MZWV",
"121 ORE => 7 VRPVC",
"7 XCVML => 6 RJRHP",
"5 BHXH, 4 VRPVC => 5 LTCX",
]
"""

# Create a DAG of Chemicals.
chemicals = {}  # str: Chemical

for line in lines:
  recipe, creates = line.strip().split(" => ")
  #print "[%s]: [%s]" % (creates, recipe)
  count, chemical_name = creates.strip().split() # the thing we're making

  if chemical_name in chemicals:
    if len(chemicals[chemical_name].needs) != 0:
      print "More than one way to make %s" % chemical_name
      sys.exit(1)
    chemical = chemicals[chemical_name]
  else:
    chemical = Chemical(chemical_name)
    chemicals[chemical_name] = chemical
  chemical.creates = int(count)

  components = recipe.split(",")
  for needed in components:
    count, name = needed.strip().split()
    #print "%s needs %d of %s" % (chemical.name, int(count), name)
    if name in chemicals:
      component = chemicals[name]
    else:
      component = Chemical(name)
      chemicals[name] = component

    chemical.needs.append((component, int(count)))
    component.needed_by.add(chemical.name)
    print component.name, "->", chemical.name
    component.needed += int(count)

print

print "There are %d chemicals" % len(chemicals)

print
print
print

unchecked = set()

for name in chemicals:
  unchecked.add(name)

unchecked.remove("FUEL")


def make_fuel(how_much=1):
  what_we_need = {"FUEL": how_much}
# we need 1 FUEL
# => we need NxA and MxB
  to_check = collections.deque()
  to_check.append("FUEL")

  while len(to_check) > 0:
    # as each node is selected, anything that needs that node is converted to
    # needing something else.
    nodename = to_check.popleft()
    if nodename == "ORE":
      break
    chemical = chemicals[nodename]
    needed = what_we_need[nodename]
    print "### Next node: %s (we need %d, this makes %d)" % (nodename,
        needed, chemical.creates)
    batches = math.ceil(float(needed) / chemical.creates)

    for dep, count in chemical.needs:
      print "To make %s, I need %d %ss" % (chemical.name, count, dep)
      print "I know how to make %d %ss" % (dep.creates, dep.name)
      dep.needed_by.remove(nodename)
      if len(dep.needed_by) == 0:
        to_check.append(dep.name)
      try:
        what_we_need[dep.name] += (count * batches)
      except KeyError:
        what_we_need[dep.name] = (count * batches)
    what_we_need.pop(nodename)
  return what_we_need["ORE"]

i = 1670299 # manual binary search. Slacker.
ore = make_fuel(i)

if ore > 1000000000000:
  print "nope"
else:
  print "yep"

