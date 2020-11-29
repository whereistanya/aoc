#!/usr/bin/env python
# Advent of code Day 24.

import math
import re
import sys

from blist import blist

######################################
# Part one
######################################

class Army(object):
  def __init__(self, name):
    self.name = name
    self.unitgroups = blist([])
    self.id_gen = self.next_id()
    self.attack_boost = 0

  def add(self, groups):
    assert len(groups) == 6
    count = int(groups[0])
    hp = int(groups[1])
    immune_system = groups[2]
    attack_power = int(groups[3]) + self.attack_boost
    damage_type = groups[4]
    initiative = int(groups[5])
    unitgroup = UnitGroup(count, hp, attack_power, damage_type, initiative)
    unitgroup.id = next(self.id_gen)
    unitgroup.army = self.name
    if immune_system:
      unitgroup.add_resistance_levels(immune_system)
    self.unitgroups.append(unitgroup)


  def units(self):
    total = 0
    for group in self.unitgroups:
      total += group.units
    return total

  def next_id(self):
    i = 0
    while True:
      i += 1
      yield i

  def select_targets(self, target_options):
    """Does not modify target_options."""
    # work in order of attack power
    chosen = set()
    for unit in sorted(self.unitgroups):
      unit.selected_target = None
      if unit.units <= 0:
        continue
      max_damage = -1
      for potential in target_options:
        # Select the target you'd do the most damage to
        if potential.units <= 0:
          continue
        if potential in chosen:
          continue
        damage = UnitGroup.calculate_damage(unit.effective_power, unit.damage_type,
                                            potential.resistance_levels)
        #print "%s group %s would do %s damage to %s group %s" % (
        #  unit.army, unit.id, damage, potential.army, potential.id)
        if damage == 0:
          continue
        if damage > max_damage:
          unit.selected_target = potential
          max_damage = damage
        # if they're equal, select the one with highest effective power
        elif damage == max_damage:
          max_damage = damage
          if potential.effective_power > unit.selected_target.effective_power:
            unit.selected_target = potential
        # if still equal, select the one with higher initiative
          elif potential.effective_power == unit.selected_target.effective_power:
            if potential.initiative > unit.selected_target.initiative:
              unit.selected_target = potential
      if unit.selected_target:
        chosen.add(unit.selected_target)

  def __repr__(self):
    s = "Army %s with units:\n" % self.name
    for unit in self.unitgroups:
      s += "* %s\n" % unit.longdesc()
    return s

class UnitGroup(object):
  def __init__(self, units, hp, attack_power, damage_type, initiative):
    self.id = 0
    self.army = None
    self.units = units
    self.hp = hp
    self.attack_power = attack_power
    self.effective_power = units * attack_power
    self.initiative = initiative
    self.damage_type = damage_type
    self.resistance_levels = {}  # {type: weak|immune}

  def longdesc(self):
    s = "%s Group %d: %dx%dhp=%d, %d %s damage, init %d\n" % (
        self.army, self.id, self.units, self.hp, self.effective_power, self.attack_power, self.damage_type, self.initiative)
    s +=  " Immunities: "
    for k, v in self.resistance_levels.items():
      s += "%s(%s), " % (k, v)
    return s

  def __repr__(self):
    return "Group %d, %d units" % (self.id, self.units)

  def __eq__(self, other):
    return self.self.initiative == other.self.initiative

  # Sorting order for which unitgroup does target selection first. Attack is a
  # different sorting order.
  def __lt__(self, other):
    if self.effective_power > other.effective_power:
      return True
    if other.effective_power > self.effective_power:
      return False
    # Equal attack power!
    if self.initiative > other.initiative:
      return True
    if other.initiative > self.initiative:
      return False
    print("The behaviour of groups with equal initiative is undefined.")
    sys.exit(1)

  def add_resistance_levels(self, immune_system):
    resistance_levels_re = "(weak|immune) to ([\w,\s]+)"
    resistance_levels = immune_system.split(";")
    for immunity in resistance_levels:
      try:
        groups = re.search(resistance_levels_re, immunity).groups()
      except AttributeError:
        print("Couldn't match:", immunities)
        sys.exit(1)
      strength = groups[0]  # weak|immune
      damage_types = groups[1] # cold, radiation, etc
      for damage_type in damage_types.split(","):
        self.resistance_levels[damage_type.strip()] = strength

  @staticmethod
  def calculate_damage(effective_power, damage_type, resistance_levels):
    #print "calc(%d, %s, %s)" % (effective_power, damage_type, resistance_levels)
    resistance = None
    if resistance_levels and damage_type in resistance_levels:
      resistance = resistance_levels[damage_type]
    if resistance == "immune":
      return 0
    if resistance == "weak":
      effective_power *= 2
    return effective_power

  def take_damage(self, attacker_effective_power, attacker_damage_type):
    damage = UnitGroup.calculate_damage(
        attacker_effective_power, attacker_damage_type, self.resistance_levels)
    units_killed = math.floor(damage / self.hp)
    self.units -= min(units_killed, self.units)
    self.effective_power = self.units * self.attack_power
    return units_killed


class Game(object):
  def __init__(self, immune_boost=0):
    self.immune_army = None
    self.infection_army = None
    with open("day24input.txt", "r") as f:
      lines = f.readlines()
    self.immune_boost = immune_boost

    """
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
    #"""
    self.populate(lines)
    self.all_units = blist(self.immune_army.unitgroups + self.infection_army.unitgroups)
    self.all_units.sort(key=lambda x: x.initiative, reverse=True) 

  def populate(self, lines):
    line_re = ("^(\d+) units each with (\d+) hit points\s*\(?(.*)\)?\s*with an attack that"
               " does (\d+) (\w+) damage at initiative (\d+)")
    for line in lines:
      if line.strip() == "":
        continue
      if line.strip() == "Immune System:":
        army = Army("Immune")
        army.attack_boost = self.immune_boost
        self.immune_army = army
        continue
      if line.strip()  == "Infection:":
        army = Army("Infection")
        self.infection_army = army
        continue
      try:
        groups = re.search(line_re, line).groups()
      except AttributeError:
        print("Couldn't match:", line)
        sys.exit(1)
      army.add(groups)

  def over(self):
    return self.infection_army.units() == 0 or self.immune_army.units() == 0

  def fight(self):
    self.immune_army.select_targets(self.infection_army.unitgroups)
    self.infection_army.select_targets(self.immune_army.unitgroups)

    # attack
    for unit in self.all_units:
      if unit.units <= 0:
        continue
      target = unit.selected_target
      if target:
        killed = target.take_damage(unit.effective_power, unit.damage_type)
        #print "%s group %d killed %d of %s group %d" % (
        #  unit.army, unit.id, killed, target.army, target.id)

  def status(self):
    s = "Immune System (%d):\n" % self.immune_army.units()
    for group in self.immune_army.unitgroups:
      s += "Group %s contains %d units\n" % (group.id, group.units)
    s += "Infection (%d):\n" % self.infection_army.units()
    for group in self.infection_army.unitgroups:
      s += "Group %s contains %d units\n" % (group.id, group.units)
    return s

game = Game()

i = 0
while not game.over():
  i += 1
  game.fight()

print("Part 1: Over after %d rounds" % i)
print(game.status())

######################################
# Part two
######################################

print("Part 2:")

def play(immune_boost):
  game = Game(immune_boost=immune_boost)
  laststatus = ""
  while not game.over():
    game.fight()
    status = game.status()
    if status == laststatus:
      break
    laststatus = status
  if game.immune_army.units() == 0:
    print("%d: Infection army wins with %d" % (immune_boost, game.infection_army.units()))
  elif game.infection_army.units() == 0:
    print("%d: Immune army wins with %d" % (immune_boost, game.immune_army.units()))
  else:
    print("%d: Stalemate." % (immune_boost))

# This could be a fancy binary search but the code is fast enough that it
# doesn't matter.
for i in range (0, 80):
  play(i)


