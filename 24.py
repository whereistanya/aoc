#!/usr/bin/env python
# Advent of code Day 24.

import re
import sys

with open("day24input.txt", "r") as f:
  lines = f.readlines()

######################################
# Part one
######################################

class Army(object):
  def __init__(self, name):
    self.name = name
    self.unitgroups = []

  def add(self, groups):
    assert len(groups) == 6
    count = int(groups[0])
    hp = int(groups[1])
    immune_system = groups[2]
    attack = int(groups[3])
    damage_type = groups[4]
    initiative = int(groups[5])
    unitgroup = UnitGroup(count, hp, attack, damage_type, initiative)
    unitgroup.add_immunities(immune_system)

    self.unitgroups.append(unitgroup)

  def __repr__(self):
    s = "Army %s with units:\n" % self.name
    for unit in self.unitgroups:
      s += "* %s\n" % unit
    return s

class UnitGroup(object):
  def __init__(self, units, hp, attack, damage_type, initiative):
    self.units = units
    self.hp = hp
    self.attack = attack
    self.initiative = initiative
    self.damage_type = damage_type
    self.immunities = {}  # {type: weak|immune}

  def __repr__(self):
    s = "UnitGroup: %dx%dhp, %d %s damage, init %d\n" % (
        self.units, self.hp, self.attack, self.damage_type, self.initiative)
    s +=  " Immunities: "
    for k, v in self.immunities.iteritems():
      s += "%s(%s), " % (k, v)
    return s

  def add_immunities(self, immune_system):
    immunities = immune_system.split(";")
    for immunity in immunities:
      try:
        groups = re.search(immunities_re, immunity).groups()
      except AttributeError:
        print "Couldn't match:", immunities
        sys.exit(1)
      strength = groups[0]  # weak|immune
      damage_types = groups[1] # cold, radiation, etc
      for damage_type in damage_types.split(","):
        self.immunities[damage_type.strip()] = strength



lines = [
  "Immune System:",
  "17 units each with 5390 hit points (weak to radiation, bludgeoning) with "
  "an attack that does 4507 fire damage at initiative 2",
  "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, "
  "slashing) with an attack that does 25 slashing damage at initiative 3",
  "",
  "Infection:",
  "801 units each with 4706 hit points (weak to radiation) with an attack "
  "that does 116 bludgeoning damage at initiative 1",
  "4485 units each with 2961 hit points (immune to radiation; weak to fire, "
  "cold) with an attack that does 12 slashing damage at initiative 4",
]

line_re = ("^(\d+) units each with (\d+) hit points \((.*)\) with an attack that"
           " does (\d+) (\w+) damage at initiative (\d+)")
immunities_re = "(weak|immune) to ([\w,\s]+)"

armies = {}

for line in lines:
  if line.strip() == "":
    continue
  if line.strip() == "Immune System:":
    army = Army("immune")
    armies["immune"] = army
    continue
  if line.strip()  == "Infection:":
    army = Army("infection")
    armies["infection"] = army
    continue
  try:
    groups = re.search(line_re, line).groups()
  except AttributeError:
    print "Couldn't match:", line
    sys.exit(1)
  army.add(groups)

for army in armies.values():
  print army

######################################
# Part two
######################################

