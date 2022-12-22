#!/usr/bin/env python3

import math
import re

test = True
test = False

class Valve(object):
  def __init__(self, name, rate):
    self.name = name
    self.rate = rate
    self.tunnels = []

if test:
  filename = "test16.txt"
else:
  filename = "input16.txt"

with open(filename, "r") as f:
  lines = [x.strip() for x in f.readlines()]

line_re = "Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)"


valves = {}
total_to_open = 0
for line in lines:
  matches = re.finditer(line_re, line)
  for match in matches:
    name, rate, out = match.groups()
    tunnels = [x.strip() for x in out.split(",")]
    if name in valves:
      valves[name].tunnels.extend(tunnels)
    else:
      valve = Valve(name, int(rate))
      valve.tunnels.extend(tunnels)
      valves[name] = valve
      if int(rate) > 0:
        total_to_open += 1

#Attempt 1, weird BFS
start = "AA"
seen = set() # global in this code
possible = [("AA", set(), seen, 0)] # current, on, seen, rate
max_pressure = 0

print(total_to_open, "to open")
for i in range (29, 0, -1): # remaining minutes
  print (i, len(possible),)
  #print(possible)
  this_round = list(possible)
  possible.clear()
  for p, on, seen, rate in this_round:
    # on is always sorted
    #print(p, on, rate)
    current = valves[p]
    #print (current.name, current.tunnels, current.rate)
    seen.add("%s-%s-%d" % (p, on, rate))
    if p not in on and current.rate > 0:
      next_on = set(on)
      next_on.add(p)
      if len(next_on) == total_to_open: # all open, drop this
        final_rate = rate + (current.rate * i)
        if final_rate > max_pressure:
          max_pressure = final_rate
          print("Max pressure is", max_pressure)
          continue
      else:
        # probably an off by one here; didn't even check
        next_rate = rate + (current.rate * i)
        if next_rate > max_pressure:
          max_pressure = next_rate
        seen.add("%s-%s-%d" % (p, sorted(next_on), next_rate))
        possible.append((p, sorted(next_on), seen, next_rate))

    for t in current.tunnels:
      next_hash = ("%s-%s-%d" % (t, on, rate))
      if next_hash not in seen:
        possible.append((t, on, seen, rate))


print("Part 1: max pressure was", max_pressure)

