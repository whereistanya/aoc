#!/usr/bin/env python3

import math
import re

test = True
test = False

if test:
  filename = "test19.txt"
else:
  filename = "input19.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]


line_re = "Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d)+ ore and (\d+) obsidian."

class Factory(object):
  def __init__(self, bp, ore_ore, clay_ore, obs_ore,
               obs_clay, geo_ore, geo_obs):
    self.name = bp
    self._costs = [
      {0: ore_ore },              # ore robot
      {0: clay_ore},              # clay robot
      {0: obs_ore, 1: obs_clay},  # obsidian robot
      {0: geo_ore, 2: geo_obs }   # geode robot
    ]
    self.costs = [
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ]
    for i in range(len(self._costs)):
      cost = self._costs[i]
      for k, v in cost.items():
        self.costs[i][k] += v
    self.max_needed = [
      max(self.costs[0][0],
          self.costs[1][0],
          self.costs[2][0],
          self.costs[3][0]),
      self.costs[2][1],
      self.costs[3][2],
      math.inf
    ]

  def can_build(self, robot_number, have):
    cost = self.costs[robot_number]
    for resource in range(4):
      if have[resource] < cost[resource]:
        return False
    return True

bps = []
for line in lines:
  matches = re.finditer(line_re, line)
  for found in matches:
    matched = [int(x) for x in found.groups()]
    bp, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = matched
    factory = Factory(bp, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)
    bps.append(factory)

# Part 1

def churn(bp, minutes, optimize_geodes_after=21):
  have = (0, 0, 0, 0)
  robots = (1, 0, 0, 0)
  max_geode_robots = 0
  max_geodes = 0

  seen = set()
  new_states = [(have, robots)]
  for minute in range(1, minutes + 1):
    to_check = new_states
    new_states = set()

    for state in to_check:
      #print(state)
      have, robots = state # both tuples
      # Optimization; don't follow paths with fewer geode robots
      # Doesn't always work (sometimes it's genuinely better to postpone
      # making a geode robot) but leave it late enough in the run and it's
      # likely to work, and save a *lot* of cycles too.
      if minute > optimize_geodes_after and have[3] < max_geodes:
        continue
      could_build = []
      # See what we could build with existing stuff.
      for i in range (4):
        # Optimization: don't build a robot if we're creating as many as we can
        # use every turn.
        if robots[i] >= bp.max_needed[i]:
          continue # never build another one of these
        if bp.can_build(i, have):
          could_build.append(i)
      # Collect new stuff
      hashed_stuff = (have[0] + robots[0], have[1] + robots[1],
                      have[2] + robots[2], have[3] + robots[3])

      # Add the state where we don't build any new robots.
      # Optimization: Only add this state when there's some resource we don't
      # have enough of and it's worth saving instead of building.
      wait = False
      for i in range(4): # if there's any resource we don't have enough of
        if robots[i] < bp.max_needed[i]:
          wait = True
          break
      if wait:
        if (hashed_stuff, robots) not in seen:
          new_states.add((hashed_stuff, robots))
          seen.add((hashed_stuff, robots))

      for robot_number in could_build:
        incremented = robots[robot_number] + 1
        hashed_robots = (robots[0:robot_number] + (incremented,) + robots[robot_number + 1:])
        if len(hashed_robots) != 4:
          print("BUG: got", hashed_robots)
          exit(1)
        costs = bp.costs[robot_number]
        have_after_building = (hashed_stuff[0] - costs[0], hashed_stuff[1] - costs[1],
                               hashed_stuff[2] - costs[2], hashed_stuff[3] - costs[3])

        if (have_after_building, hashed_robots) not in seen:
          new_states.add((have_after_building, hashed_robots))
          seen.add((have_after_building, hashed_robots))

    #print("After minute %d, there are %d possible states" % (minute,
    #      len(new_states)))
    #print(new_states)
    max_geode_robots = 0
    max_geodes = 0
    for state in new_states:
      have, robots = state
      if robots[3] > max_geode_robots:
        max_geode_robots = robots[3]
      if have[3] > max_geodes:
        max_geodes = have[3]
    #print("Max geode robots so far is %d (%d)" % (max_geode_robots, max_geodes))
    #print("Max geodes so far is %d (with %d robots)" % (max_geodes, max_geode_robots))

  max_geodes = 0
  for state in new_states:
    have, robots = state
    if have[3] > max_geodes:
      max_geodes = have[3]
  return max_geodes

# Part 1
total = 0
print("Part 1")
for bp in bps:
  print("Blueprint %d: %s" % (bp.name, bp.costs))
  max_geodes = churn(bp, 24, optimize_geodes_after=22)
  total += (bp.name * max_geodes)

print("Part 1:", total)

# Part 2

print("Part 2")
total = 1
for bp in bps[0:3]:
  print("Blueprint %d: %s" % (bp.name, bp.costs))
  max_geodes = churn(bp, 32, optimize_geodes_after=21)
  total *= max_geodes

print("Part 2:", total)


